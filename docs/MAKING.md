# 制作步骤

## 制作与复现

1. 逐条核对 BoardUI 控件能力，选用明确业务场景；所有数据和提交反馈均为模拟。
2. 编排 0–2 秒钩子，2–17 秒五段，每段 3 秒；17–20 秒总结提示词公式。
3. 保留原控件动画，新增场景行和提示词面板；字体本地加载。
4. 九帧检查后放大提示词字体，复查所有句子是否完整显示。
5. Python 固定随机种子生成 120 BPM 配乐和动作音；最后一个小节落主和弦并淡出。
6. Playwright 导出 1200 帧 JPG，FFmpeg 编码 H.264 Main / yuv420p / AAC，并启用 faststart。
7. 从最终 MP4 抽帧复核，并检查完整播放与多点跳转。

依赖 Node.js、Python 3、NumPy、FFmpeg 和 Chrome。

```sh
npm install
python3 -m pip install numpy
python3 make_audio.py
node render.mjs
node render.mjs full
sh encode.sh
```

默认使用 macOS Chrome，其他系统设置 `CHROME_PATH`。安装 huashu-motion 后可用 `npx huashu-motion studio . --no-open` 预览时间线。

`index.html` 是动画画布，`window.draw(t)` 可定位 0–20 秒任意时刻。本包展示模拟操作，不包含真实登录或服务端上传。

字体 Noto Sans SC 随附 OFL 许可，GSAP 和 OM 许可在 vendor 中，英文标题使用系统 Georgia。参考 BoardUI 的交互类型，未复制原站源码。

网页使用原生 HTML/CSS/JavaScript 实现同款控件。影片使用确定性 Canvas 绘制；两者保持相同布局、初始值和操作结果。上传和登录仅为本地模拟。

## 本地网页

在仓库根目录运行 `python3 -m http.server 8000`，访问 http://localhost:8000/。

## 重新生成视频

进入 film 后运行文中的安装、音频生成、逐帧渲染和编码命令。输出 MP4 后复制到 media/controls-knowledge-20s.mp4。
