# RYU / OKI LAB — 隆的压起身训练站

一个真正可交互的**静态网站**。主界面简体中文，以经典操作（键盘）为主。版本快照：**2026-11-19**。

## 已实现

- **20 项压起身研究条目**（版中、版边），包含中升龙、重升龙、重驴踢、旋风、轻驴踢、版边前投、反 DI 等。
- 每个动作代码下方的**逐招中文注释**，以及打击、投技、Shimmy、命中后连段、防御风险分支。
- **31 条命中后续连段候选**，区分无 Drive、SA3 和高投入研究路线；仅在资料明确给出精确伤害且条件一致时才可称最高。当前没有把未经验证的伤害数字伪造成“最优”。
- 搜索、位置筛选、收尾筛选、收藏、已练习标记、私人备注（本机 localStorage），训练数据 JSON 导出。
- 当前版本区别：**2026-10-13 检测到游戏更新**，但多数隆的详细压起身攻略仍是 **2026-08-03 基准**。新补丁不意味着原本每一项压起身自动复测通过。
- 手动补丁记录；部署 GitHub Pages 后可以用随附 GitHub Actions **每 12 小时检查一次官方 Steam 新闻**，自动更新 `data/patch-status.json`，并提醒人手核验。行动有运行延迟、数据源缺漏及访问失败可能；不会自动更新未核实的连段、帧数或“最高伤害”。

## 本地查看

把整个文件夹解压后，在浏览器打开 `index.html`。支持无网络访问（外链和自动补丁检查除外）。

## 发布到 GitHub Pages

1. 在 GitHub 创建新的公开或允许 Pages 的仓库，上传此文件夹内全部文件，包括 `.github/workflows/check-patches.yml`。**注意**上传隐藏文件夹 `.github`。
2. 仓库 **Settings → Pages**，选择 `Deploy from a branch`，`main` 分支、`/(root)`，点击保存。
3. 仓库 **Settings → Actions → General → Workflow permissions**，允许 `Read and write permissions`。GitHub Actions 的运行安排可能受仓库权限和平台限制；如未启动，去 Actions 页执行 `Run workflow`。
4. 网站可通过 `https://<你的 GitHub 用户名>.github.io/<仓库名>/` 访问。检查「补丁追踪」的自动发现状态。
5. GitHub 的定时任务**并非实时流**；此项目最高频率设为每 12 小时。只有当官方 Steam 新闻包含可识别平衡关键词时才会提出复核。对于由社媒、游戏内公告或其他形式发布的改动，仍需要人工核查。

## 更新套路数据库

`data/routes.json` 是可读的结构化源数据。更新后需同步生成 `data/routes.js`：

```bash
python - <<'PY'
import json,pathlib
p=pathlib.Path('data/routes.json')
pathlib.Path('data/routes.js').write_text('window.RYU_DATA = '+json.dumps(json.loads(p.read_text()),ensure_ascii=False,separators=(',',':'))+';\n')
PY
```

目前浏览器界面不能把新修改写回仓库（静态站无后台），但是可以记录自己的复测笔记并导出。

## 术语与限制

- “最高伤害”须先约定：**相同起手、同位置、同招式命中方式、同 Drive/SA 资源量、同电刃状态、同普通/Counter/Punish Counter**。当前列出高伤害候选，未达到全面验证最优的条件。
- +32F 中升龙仅指**特定 236HK 后空中追击高度**，不是所有 `623MP` 命中。
- +37F 重升龙主要指**地面完整命中**，空中命中结果不同。
- +45F 重驴踢仅指对应**地面命中条件**，版中两次前冲后 5MP 的距离不保证成立。
- 对于曾讨论的 **中升龙 +32 → 2LP 空挥×2 → 5MP**：`2LP` 空挥按约 14F 计算，共耗 28F，剩余 +4F，**不能自动构成 6F 发生 5MP 的压起身**。站点保留为待验证条目，并明显标出警告，而不是默许为固定 meaty。
- 版边 **中升龙 +32 → 5MK 空挥 → 5MP / 投** 是用户偏好的练习思路，但 5MK 空挥后约 +3F，6F 发生的站中拳**并非必定压过起身 4F 技**；打投的具体可靠性要检查。

## 参考来源

- 官方 2026-08 隆变更列表： https://www.streetfighter.com/6/buckler/ja-jp/battle_change/20260803/ryu
- 官方 2026-10 变更列表： https://www.streetfighter.com/6/buckler/battle_change/20261013
- 隆攻略/压起身条目： https://sf6-genten.com/character/ryu/category/okizeme-setplay
- 隆招式数据： https://shoryu.site/character/ryu
- 中升龙 2026 setplay 分析： https://note.com/light_rabbit7722/n/n820dba298d11

非 Capcom 官方作品；所有动作在真实游戏版本中以实战训练模式为准。
