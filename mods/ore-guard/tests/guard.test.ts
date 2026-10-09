import { expect, test } from 'claude-code/testing';
const pointer = '{"schema_version":1,"task_id":"fixture"}';
const task = JSON.stringify({schema_version:1,id:'fixture',title:'Fixture',objective:'Verify',status:'active',revision:1,deliverables:[{name:'Build',weight:100,completion:0,status:'pending'}],gates:{},blockers:[]});
for (const answer of ['Cancel','Proceed once']) {
  test(`guard handles ${answer}`, async ($, on) => {
    let executed = false;
    on('session.cwd', () => ({value:'/workspace'}));
    on('fs.read', ($, e) => ({value:e.path.endsWith('active.json') ? pointer : task}));
    on('tool.call', {tool:'AskUserQuestion'}, ($, e) => ({result:{questions:e.questions, answers:{[e.questions[0]!.question]:answer}}}));
    on('tool.call', {tool:'Bash'}, () => {executed=true;return {result:'mocked'};});
    const result = await $.tool.call({tool:'Bash',command:'npm publish'});
    expect(executed).toBe(answer==='Proceed once');
    if(answer==='Cancel') expect(result.deny).toBeDefined();
  });
}
