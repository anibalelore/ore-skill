import { expect, test, mock } from 'claude-code/testing';

test('renders persisted progress on terminal and desktop', async ($, on) => {
  mock.clock(on);
  on('session.cwd', () => ({ value: '/workspace' }));
  on('fs.read', ($, e) => ({ value: e.path.endsWith('active.json')
    ? '{"schema_version":1,"task_id":"fixture"}'
    : JSON.stringify({ schema_version: 1, id: 'fixture', title: 'Fixture', objective: 'Verify', status: 'active', revision: 1,
      deliverables: [{name:'Build',weight:100,completion:25,status:'in_progress'}], gates: {}, blockers: [] }) }));
  on('command.register', ($, e) => ({value:{command:e.name}}));
  on('session.start', ($, e) => ({cwd:e.cwd}));
  on('ui.render', {component:'AbovePrompt'}, () => ({type:'Text', props:{}, children:['Existing band']}));
  await $.session.start({cwd:'/workspace',surface:'terminal',isInteractive:true});
  for (const surface of ['terminal','desktop'] as const) {
    const drawing = await $.ui.mount({ plugin: 'ore-progress', surface, component: 'AbovePrompt', requestId: 'band',
      props: {hasSurvey:false,isWorking:false,maxRows:10,bodyColumns:100,scroll:{offset:0,bodyRows:10},view:{}} });
    expect(await drawing.find({type:'Text',text:/Fixture.*25%/})).toBeDefined();
    expect(await drawing.find({type:'Text',text:'Existing band'})).toBeDefined();
    await drawing.unmount();
  }
});
