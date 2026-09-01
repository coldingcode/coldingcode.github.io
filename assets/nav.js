// 共享侧边导航：renderNav(active) 把当前页标为 active。
// 用法：<div id="nav-placeholder"></div><script src="assets/nav.js"></script><script>renderNav('20')</script>
// 新增页面时只需改这里 + 全书目录 index.html 的目录章节。
const NAV_ITEMS = {
  '00': '00-root.html', '01': '01-boot.html', '02': '02-parse.html', '03': '03-cordis.html', '04': '04-run-profile.html',
  '05': '05-spine.html', '06': '06-session.html', '07': '07-agent.html', '08': '08-prestep.html', '09': '09-buildreq.html',
  '10': '10-stream.html', '11': '11-step.html', '12': '12-schema.html', '13': '13-tool-sched.html', '14': '14-pipeline.html',
  '15': '15-seam.html', '16': '16-bash-provider.html', '17': '17-shell-consumer.html',
  '20': '20-persist.html', '21': '21-compaction.html', '22': '22-subagent.html', '23': '23-skill.html',
  '24': '24-goal-plan.html', '25': '25-workflow-jobs.html', '26': '26-fs.html', '27': '27-terminal-lsp.html',
  '28': '28-web.html', '29': '29-approval.html', '30': '30-storage.html', '31': '31-settings.html',
  '32': '32-sdk-api.html', '33': '33-client-python.html', '34': '34-infra.html',
};

const NAV_TITLES = {
  '00': '根：bin.ts 入口', '01': 'args 解析', '02': 'loadProfile：五层', '03': 'boot + Cordis 运行时', '04': 'runProfile：树热更新',
  '05': '脊柱：从 kick 出发', '06': 'Session：日志与 append', '07': 'Inbox：双队列投影', '08': 'preStep：四个动作',
  '09': 'buildRequest：日志→请求', '10': 'llm/stream：流式调用', '11': 'step：循环、落盘、分支', '12': 'assemble：提示词组装',
  '13': 'executeToolCalls：调度', '14': 'ToolRuntime：三段流水线', '15': '分岔点：seam 与注入', '16': '↳ bash-local Provider', '17': '↳ tool-bash Consumer',
  '20': '持久化与恢复', '21': '压缩与上下文', '22': '子代理', '23': '技能与命令', '24': '目标与计划',
  '25': '工作流与任务', '26': '文件系统', '27': '终端与 LSP', '28': 'Web 能力', '29': '审批、权限与沙箱',
  '30': '存储与会话查询', '31': '设置、凭据与身份', '32': 'SDK 与 API 服务', '33': '客户端、Python 与 Native', '34': '工程基础设施',
};

function navLink(id) {
  const file = NAV_ITEMS[id];
  const title = NAV_TITLES[id];
  const active = window.__NAV_ACTIVE__ === id ? ' class="active"' : '';
  const branch = (id === '16' || id === '17') ? ' class="branch"' : '';
  const idx = window.__NAV_ACTIVE__ === id
    ? (id === '16' || id === '17' ? `<span class="idx">${id}</span>` : `<span class="idx">${id}</span>`)
    : `<span class="idx">${id}</span>`;
  return `<li${branch}><a href="${file}"${active}>${idx}${title}</a></li>`;
}

function renderNav(active) {
  window.__NAV_ACTIVE__ = active;
  const el = document.getElementById('nav-placeholder');
  if (!el) return;
  el.outerHTML = `<aside class="nav">
  <div class="nav-head">
    <div class="nav-logo">DSH</div>
    <div class="nav-title">源码精读</div>
    <div class="nav-sub">DeepSeek Harness</div>
  </div>
  <div class="nav-group">总览</div>
  <ul class="nav-list">
    <li><a href="index.html"${active === 'home' ? ' class="active"' : ''}><span class="idx">⌂</span>全书目录</a></li>
    <li><a href="changelog.html"${active === 'log' ? ' class="active"' : ''}><span class="idx">★</span>版本更新</a></li>
  </ul>
  <div class="nav-group">卷零 · 入口与组装</div>
  <ul class="nav-list">
    ${['00','01','02','03','04'].map(navLink).join('\n    ')}
  </ul>
  <div class="nav-group">卷一 · 核心循环深读</div>
  <ul class="nav-list">
    ${['05','06','07','08','09','10','11','12','13','14'].map(navLink).join('\n    ')}
  </ul>
  <div class="nav-group">卷一（旁支） · Shell 能力缝</div>
  <ul class="nav-list">
    ${['15','16','17'].map(navLink).join('\n    ')}
  </ul>
  <div class="nav-group">卷二 · 能力全景</div>
  <ul class="nav-list">
    ${['20','21','22','23','24','25','26','27','28','29','30','31','32','33','34'].map(navLink).join('\n    ')}
  </ul>
  <div class="nav-foot">基于 dsh 0.1.2-alpha.3<br>离线可用 · 无外部依赖</div>
</aside>`;
}
