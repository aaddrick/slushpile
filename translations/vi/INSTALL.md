# Cài đặt

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../INSTALL.md">English</a> ·
  <a href="../zh-CN/INSTALL.md">简体中文</a> ·
  <a href="../es/INSTALL.md">Español</a> ·
  <a href="../pt-BR/INSTALL.md">Português (BR)</a> ·
  <strong>Tiếng Việt</strong> ·
  <a href="../en-x-aibro/INSTALL.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

slushpile là 9 kỹ năng và 8 định nghĩa tác nhân, tất cả đều là Markdown. Mọi
cách cài bên dưới đều đặt cùng bộ tệp đó vào nơi tác nhân của bạn sẽ đọc được.

**Một điều phải quyết trước khi cài bất cứ thứ gì:** không gian làm việc của bạn
nằm ở đâu.

Plugin là mã nguồn. Không gian làm việc của bạn là lịch sử việc làm, mức lương
và các ràng buộc của bạn. Đó là hai thứ khác nhau và chúng thuộc về hai thư mục
khác nhau. Hãy cài plugin vào nơi tác nhân của bạn giữ plugin; chạy
`/slushpile:onboard` trong một thư mục riêng mà bạn giữ kín.

---

## Claude Code

Toàn bộ quy trình. Kỹ năng trở thành lệnh gạch chéo, 8 tác nhân được điều phối
dưới dạng tác nhân con, và 5 người đánh giá song song thực sự chạy song song.

```bash
claude plugin marketplace add VonTerraProject501c3/slushpile
```

```bash
claude plugin install slushpile@slushpile
```

Kiểm tra lại:

```bash
claude plugin list
```

Bạn sẽ thấy `slushpile@slushpile` và `enabled`.

Rồi bắt đầu:

```
/slushpile:onboard
```

Chạy nó trong thư mục nơi bạn muốn đặt quá trình tìm việc của mình.

### Cập nhật

```bash
claude plugin marketplace update slushpile
```

```bash
claude plugin install slushpile@slushpile
```

### Gỡ cài đặt

```bash
claude plugin uninstall slushpile
```

```bash
claude plugin marketplace remove slushpile
```

Không lệnh nào trong hai lệnh đó đụng đến các tệp trong không gian làm việc của
bạn.

---

## Codex

```bash
codex plugin marketplace add VonTerraProject501c3/slushpile --ref main
```

```bash
codex plugin add slushpile@slushpile
```

Bên trong Codex, `/plugins` mở trình duyệt plugin.

Codex thêm tiền tố là tên plugin vào trước kỹ năng của plugin:

```
$slushpile:onboard
```

**Chỗ khác biệt.** Codex không có cơ chế điều phối tác nhân con. Quy trình đánh
giá chạy 7 người đánh giá của nó tuần tự trong một ngữ cảnh duy nhất: đọc từng
định nghĩa tác nhân trong thư mục `agents/` của plugin, nhập vai, viết báo cáo,
rồi chuyển sang cái tiếp theo.

Kết quả vẫn cùng hình dạng. Hai thứ suy giảm, và đáng biết là hai thứ nào:

1. Chậm hơn. Bảy lượt chạy tuần tự thay vì 5 người đánh giá song song rồi thêm
   hai lượt nữa.
2. Lẽ ra 5 người đánh giá song song phải mù với nhau, không thấy được kết quả
   của nhau. Trong cùng một ngữ cảnh thì họ không mù, và một chuyên gia đã đọc
   phán quyết phân loại sẽ trôi dần về phía đồng tình với nó. Hãy viết trọn
   từng báo cáo trước khi bắt đầu báo cáo kế tiếp, đúng như kỹ năng chỉ dẫn.

---

## Gemini CLI

```bash
gemini extensions install https://github.com/VonTerraProject501c3/slushpile
```

Extension khai báo `GEMINI.md` là tệp ngữ cảnh của nó, và tệp đó nạp vào mọi kỹ
năng cùng mọi định nghĩa tác nhân.

Rồi, trong thư mục không gian làm việc của bạn:

```
Set up a slushpile workspace here.
```

Gemini cũng không có cơ chế điều phối tác nhân con, nên vẫn nguyên cảnh báo về
chạy tuần tự ở trên.

### Cài thủ công

Clone vào thư mục extension:

```bash
git clone https://github.com/VonTerraProject501c3/slushpile ~/.gemini/extensions/slushpile
```

---

## Cursor

Cursor đọc `.cursor/skills/` và `.cursor/rules/` từ không gian làm việc mà nó
đang mở. Hãy clone kho lưu trữ rồi chép chúng vào không gian làm việc của bạn:

```bash
git clone https://github.com/VonTerraProject501c3/slushpile /tmp/slushpile
```

```bash
cp -r /tmp/slushpile/.cursor/skills/slushpile <your-workspace>/.cursor/skills/
```

```bash
cp -r /tmp/slushpile/skills /tmp/slushpile/agents /tmp/slushpile/templates <your-workspace>/.slushpile/
```

Kỹ năng Cursor chỉ là một bộ định tuyến: nó trỏ tới các tệp kỹ năng thật nằm
dưới `.slushpile/`. Nhờ vậy chỉ có một bản sao của quy trình thay vì bốn.

Sau đó gõ `/slushpile` trong Cursor và nói bạn muốn làm gì.

---

## Mọi harness khác

Quy trình là Markdown thuần với frontmatter YAML. Bất kỳ tác nhân nào đọc được
tệp đều chạy được nó.

Clone kho lưu trữ vào một chỗ mà tác nhân của bạn với tới được:

```bash
git clone https://github.com/VonTerraProject501c3/slushpile ~/.slushpile
```

Rồi đặt đoạn dưới đây vào `AGENTS.md` của bạn, vào system prompt, hoặc vào bất
cứ chỗ nào harness của bạn dùng cho các chỉ dẫn thường trực:

<!-- BEGIN GENERATED harness-snippet: scripts/sync_docs.py -->

```markdown
## slushpile

A job application pipeline lives at `~/.slushpile`. When the user asks to set up
a job search, search a careers board, build an application, or review one, read
the matching skill and follow it:

- `~/.slushpile/skills/onboard/SKILL.md` — set up the workspace, once
- `~/.slushpile/skills/job-board-search/SKILL.md` — search and score roles
- `~/.slushpile/skills/explore-experience/SKILL.md` — interview for undocumented experience
- `~/.slushpile/skills/application-builder/SKILL.md` — build the resume and cover letter
- `~/.slushpile/skills/adversarial-review/SKILL.md` — run the seven-agent review
- `~/.slushpile/skills/removing-ai-tells/SKILL.md` — strip AI-authorship signals from prose
- `~/.slushpile/skills/redesign-templates/SKILL.md` — restyle the document templates
- `~/.slushpile/skills/status/SKILL.md` — report the queue and check pipeline calibration
- `~/.slushpile/skills/help/SKILL.md` — what to run next, and how to read the output

The review dispatches personas defined in `~/.slushpile/agents/`. If you cannot
dispatch subagents, adopt each definition in turn and run them sequentially,
writing each report out before starting the next.

Cover letters are written by the voice agent named in `preferences.yaml` under
`voice.agent`. A working example ships as `aaddrick-voice`; it is the plugin
author's voice, and users generate their own with
https://github.com/aaddrick/written-voice-replication

Workspace templates are in `~/.slushpile/templates/`.
```

<!-- END GENERATED harness-snippet -->

---

## Phần còn lại của sổ tay

Mọi thứ sau bước cài đặt nằm trong [docs/](docs/index.md):

- [Bắt đầu](docs/getting-started.md): cần gom những gì trước khi onboarding, và
  quy trình cần cài sẵn những gì — `pdftotext`, và tùy chọn thêm một bộ công cụ
  LaTeX cùng các phông chữ tài liệu đóng gói kèm.
- [Kỹ năng](docs/skills.md): mọi lệnh `/slushpile:*` và khi nào chạy nó.
- [Không gian làm việc](docs/workspace.md): những tệp mà onboarding ghi vào thư
  mục của bạn, và thứ gì đọc từng tệp.
- [Tác nhân giọng văn của bạn](docs/voice.md): vì sao thư xin việc cần một cái,
  và cách tạo cái của riêng bạn.
- [Xử lý sự cố](docs/troubleshooting.md).
- [Kiến trúc](docs/architecture/index.md): vì sao quy trình có hình dạng như
  hiện tại.
