import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ApprovalExperience(unittest.TestCase):
    def invoke(self, harness, payload):
        result = subprocess.run(['node', str(ROOT / 'evals' / harness)], input=json.dumps(payload), capture_output=True, text=True, encoding='utf-8', cwd=ROOT)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def summary(self, action, **changes):
        return self.invoke('approval_harness.mjs', dict(action=action, **changes))

    def guard(self, command, **changes):
        from test_mods_state import FIXTURE
        return self.invoke('mods_harness.mjs', dict(mod='ore-guard', task=FIXTURE, tool=command, **changes))

    def ledger(self, request, **changes):
        from test_mods_state import FIXTURE
        return self.invoke('runtime_mods_harness.mjs', dict(mod='ore-approval-ledger', task=FIXTURE, request=request, **changes))

    def test_sql_multilineal_exacto_y_controles_no_verificados(self):
        sql = 'CREATE TABLE public.activity_log (\n  id bigint PRIMARY KEY,\n  actor uuid NOT NULL\n);'
        result = self.summary(dict(query=sql, project_id='isolated-test'), tool='mcp__supabase__execute_sql', details=True)
        self.assertEqual(json.loads(result['summary']['exact'])['query'], sql)
        self.assertIn(sql, result['text'])
        self.assertIn('public.activity_log', result['text'])
        self.assertEqual(result['summary']['risk'], 'Medio')
        self.assertEqual(result['summary']['platform'], 'Supabase')
        self.assertIn('no se han probado', result['text'])
        self.assertNotIn('inmutable', result['text'])

    def test_escape_solo_prosa_no_modifica_comando(self):
        command = 'printf "a\\nb"'
        result = self.summary(dict(command=command), reason='Primera línea\\nSegunda línea', details=True)
        self.assertIn('Primera línea\nSegunda línea', result['text'])
        self.assertEqual(json.loads(result['summary']['exact'])['command'], command)
        self.assertIn(command, result['text'])

    def test_comando_extenso_completo_o_bloqueado(self):
        command = 'echo ' + 'safe ' * 500 + '; rm -rf important'
        result = self.summary(dict(command=command))
        self.assertIsNone(result['summary']['blocked'])
        self.assertIn(command, result['text'])
        self.assertEqual(result['summary']['risk'], 'Crítico')
        large = self.guard('rm -rf ' + 'x' * 15000, answer='Aprobar una vez')
        self.assertEqual(large['passed'], 0)
        self.assertEqual(large['asks'], 0)
        self.assertIn('deny', large['result'])

    def test_produccion_y_permisos_independientes_del_nombre(self):
        for action in (dict(query='CREATE TABLE t (id int)', environment='production'), dict(command='chmod 777 ./data', environment='local'), dict(query='ALTER TABLE x DISABLE ROW LEVEL SECURITY', environment='test')):
            result = self.summary(action)
            self.assertEqual(result['summary']['risk'], 'Alto')
            self.assertIn('Detalles técnicos completos', result['text'])
        benign_name = self.summary(dict(query='DROP TABLE accounts', environment='test', description='Safe read'), tool='safe_read')
        self.assertEqual(benign_name['summary']['risk'], 'Crítico')

    def test_recursos_desconocidos_no_se_inventan(self):
        result = self.summary(dict(command='deploy_app'))
        self.assertIn('Detectar y verificar', result['text'])
        self.assertIn('Recursos no identificados', result['text'])
        self.assertNotIn('reversión garantizada', result['text'])
        self.assertEqual(self.summary(dict(command='run_unknown_script', target='local'))['summary']['risk'], 'Alto')

    def test_permisos_insuficientes_y_secretos_bloquean(self):
        for action in (dict(command='npm publish', permissions_sufficient=False), dict(command='deploy', api_key='private-credential'), dict(command='psql postgres://user:secret@host/database'), dict(command='curl -H "Authorization: Bearer private"')):
            result = self.summary(action)
            self.assertIsNotNone(result['summary']['blocked'])
            self.assertEqual(result['summary']['exact'], '')
            self.assertNotIn('private-credential', result['text'])

    def test_rechazo_revision_y_fallo_presentacion(self):
        for changes in ({'answer': 'Rechazar'}, {'answer': 'Aprobar dentro de una política'}, {'answer': 'Aprobar una vez', 'dismiss': True}, {'answer': 'Aprobar una vez', 'changeDuringAsk': True}, {'answer': 'Aprobar una vez', 'changeActionDuringAsk': True}):
            result = self.guard('rm -rf data', **changes)
            self.assertIn('deny', result['result'])
            self.assertEqual(result['passed'], 0)

    def test_detalles_peligrosos_visibles_antes_de_aprobar(self):
        result = self.guard('psql -c "DROP TABLE accounts"', answer='Aprobar una vez')
        self.assertEqual(result['passed'], 1)
        self.assertIn('DROP TABLE accounts', result['questions'][0]['question'])
        self.assertIn('Crítico', result['questions'][0]['question'])
        details = self.guard('rm -rf data', answers=['Revisar detalles', 'Rechazar'])
        self.assertEqual(details['asks'], 2)
        self.assertEqual(details['passed'], 0)

    def test_resumen_ledger_no_autoriza_sin_detalles(self):
        request = dict(action='approval', payload=dict(id='approve-a', operation='deploy', scope='task:test', environment='production', expires_at='2099-01-01T00:00:00Z', owner='owner', evidence='explicit'))
        invalid = self.ledger(request, answer='Aprobar una vez')
        self.assertEqual(invalid['processes'], 0)
        valid = self.ledger(request, answers=['Revisar detalles', 'Aprobar una vez'])
        self.assertEqual(valid['processes'], 1)
        self.assertEqual(valid['asks'], 2)
        self.assertEqual(valid['lastPayload'], request['payload'])
        self.assertIn('2099-01-01', valid['lastQuestion'])
        self.assertIn('task:test', valid['lastQuestion'])
        self.assertNotIn('Aprobar durante la sesión', valid['questions'][0]['options'])

    def test_ledger_presentacion_fallida_no_escribe(self):
        result = self.ledger(dict(action='approval', payload={}), dismiss=True)
        self.assertEqual(result['processes'], 0)
        self.assertEqual(result['result']['exitCode'], 2)

    def test_descripcion_usuario_no_reclasifica_accion(self):
        a = self.summary(dict(command='git status', target='local', description='DROP TABLE prod'))
        self.assertEqual(a['summary']['risk'], 'Bajo')
        self.assertNotIn('DROP TABLE', a['text'])
        self.assertIn('DROP TABLE', self.summary(dict(command='git status', target='local', description='DROP TABLE prod'), details=True)['text'])

    def test_fences_y_caracteres_control(self):
        command = 'echo "```"; rm -rf data'
        result = self.summary(dict(command=command))
        self.assertIn('````text', result['text'])
        self.assertIn(command, result['text'])
        self.assertIsNotNone(self.summary(dict(command='rm -rf \u001b[2Jdata'))['summary']['blocked'])

    def test_politica_configurable_no_elimina_protecciones_base(self):
        result = self.guard('rm -rf data', options={'patterns': '[]'}, answer='Rechazar')
        self.assertEqual(result['asks'], 1)
        self.assertEqual(result['passed'], 0)

    def test_efectos_git_cloud_y_destructivos_al_final(self):
        for command in ('rm --recursive data', 'git push origin +main', 'terraform destroy -target resource', 'kubectl delete namespace production'):
            result = self.summary(dict(command=command))
            self.assertEqual(result['summary']['risk'], 'Crítico')
            self.assertIn(command, result['text'])
        result = self.guard('supabase db push --project-ref production', answer='Rechazar')
        self.assertEqual(result['passed'], 0)
        self.assertIn('Producción', result['questions'][0]['question'])

    def test_resumen_no_recupera_aprobacion_expirada(self):
        import sys
        sys.path.insert(0, str(ROOT / 'skills/ore/scripts'))
        from ore_runtime import initial_governance, apply_governance
        from ore_models import route, operation
        from test_ore_models import NOW, TASK, CANDIDATE, request
        data = apply_governance(initial_governance('project'), 'approval', dict(id='route-test', owner='owner', evidence='explicit', operation=operation(CANDIDATE), scope='task:test-task', environment='codex:main_session', expires_at='2026-10-10T12:00:00+00:00'), 'project', NOW, True)
        data['approvals'][0]['expires_at'] = NOW
        self.summary(dict(action='approval', payload=data['approvals'][0]), details=True)
        self.assertEqual(route(request(), TASK, data, 'project', NOW)['approval_status'], 'awaiting-approval')


if __name__ == '__main__': unittest.main()
