<p align="center">
  <img src="../../.github/assets/hero-vi.png" alt="Slushpile: một cuộc tìm việc đối kháng có trí nhớ. 7 tác nhân cố loại bạn trước khi một nhà tuyển dụng kịp làm vậy, và những gì chúng tìm ra thì bạn giữ lại. Những gì bạn giữ lại: profile.md, mọi tuyên bố sự kiện; preferences.yaml, lương, địa điểm và ràng buộc; stories.md, bốn đến tám câu chuyện kể được; job_search.md, kết quả thực tế để hiệu chỉnh. Viết một lần, mọi giai đoạn đều đọc, mọi vòng đánh giá đều cập nhật. 7 người đánh giá: người sàng lọc nhanh, chuyên viên phân tích yêu cầu, trình mô phỏng ATS, người đọc đã mệt, chuyên viên phân tích nhóm ứng viên, quản lý tuyển dụng, người phản biện. 5 người đánh giá song song, mù với nhau, rồi tổng hợp, rồi một tác nhân có nhiệm vụ lật ngược kết quả đó." width="100%">
</p>

<p align="center">
  <strong>Slushpile</strong><br>
  <em>7 tác nhân cố loại bạn trước khi một nhà tuyển dụng kịp làm điều đó.</em><br>
  <em>Những gì chúng tìm ra thì bạn giữ lại.</em>
</p>

<p align="center">
  <a href="../../LICENSE"><img src="https://img.shields.io/github/license/VonTerraProject501c3/slushpile?style=flat" alt="Giấy phép"></a>
  <a href="../../.github/workflows/plugin-load-check.yml"><img src="https://img.shields.io/github/actions/workflow/status/VonTerraProject501c3/slushpile/plugin-load-check.yml?label=plugin%20loads&style=flat" alt="Kiểm tra nạp plugin"></a>
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/aaddrick/">Kết nối trên LinkedIn!</a>
</p>

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../README.md">English</a> ·
  <a href="../zh-CN/README.md">简体中文</a> ·
  <a href="../es/README.md">Español</a> ·
  <a href="../pt-BR/README.md">Português (BR)</a> ·
  <strong>Tiếng Việt</strong> ·
  <a href="../en-x-aibro/README.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

<!-- BEGIN GENERATED market-note: scripts/sync_docs.py -->

> **Phạm vi**: quy trình này mô phỏng quy ước tuyển dụng của các thị trường nói tiếng Anh, chủ yếu là Mỹ: một trang, không ảnh, không ngày sinh, sắp xếp ngược theo thời gian, và một dòng về tình trạng được phép làm việc. Nếu bạn ứng tuyển ở thị trường trong nước với quy ước khác, lời khuyên về định dạng không áp dụng và vòng đánh giá sẽ coi những gì bình thường ở đó là lỗi. Theo dõi tại [issue #2](https://github.com/VonTerraProject501c3/slushpile/issues/2).

<!-- END GENERATED market-note -->

## Cài đặt

<details open>
<summary><strong>Claude Code</strong></summary>

```bash
claude plugin marketplace add VonTerraProject501c3/slushpile
```

```bash
claude plugin install slushpile@slushpile
```

Sau đó, trong thư mục bạn dùng để tìm việc:

```
/slushpile:onboard
```

</details>

<details>
<summary><strong>Codex</strong></summary>

```bash
codex plugin marketplace add VonTerraProject501c3/slushpile --ref main
```

```bash
codex plugin add slushpile@slushpile
```

Codex thêm tiền tố tên plugin vào kỹ năng của plugin:

```
$slushpile:onboard
```

Codex không điều phối tác nhân con, nên quy trình đánh giá chạy tuần tự 7 người
đánh giá trong cùng một ngữ cảnh thay vì 5 người đánh giá song song. Cùng một
đầu ra, chậm hơn, và dễ bị lập luận của người này rò sang người kế tiếp hơn một
chút.

</details>

<details>
<summary><strong>Cursor, Gemini CLI, và cài đặt thủ công</strong></summary>

Xem [INSTALL.md](./INSTALL.md).

</details>

## Vấn đề

Bạn không bị chấm điểm so với bản mô tả công việc. Bạn bị chấm điểm so với bảy
mươi người khác đã nộp vào cùng một vị trí trong tuần này.

Gần như mọi công cụ trong mảng này hiểu ngược điều đó. Đưa một hồ sơ và một tin
tuyển dụng vào một công cụ tối ưu hồ sơ, nó sẽ báo rằng độ khớp từ khóa của bạn
đã tăng từ 68% lên 91%, một con số có thật về một câu hỏi sai. Nếu ứng viên ở
phân vị thứ 75 trong hàng đợi đó khớp ở mức 94%, thì 91% của bạn là một lá thư
từ chối, và không có gì trong công cụ đó nói cho bạn biết điều này.

Điều thứ hai họ làm sai: họ trả về một phán quyết duy nhất. Nhưng cùng một hồ sơ
và cùng một lá thư có thể chuyển đổi khoảng 2% qua kênh nộp nguội trên cổng
tuyển dụng và 30% qua kênh giới thiệu nội bộ. Đó không phải là cùng một quyết
định, và gộp chúng lại thành một chữ "rất khớp" không phải là sự đơn giản hóa.
Đó là một sai lầm được khoác lên một giao diện tự tin.

Điều thứ ba là điều không ai gọi tên. Những công cụ này không có trí nhớ. Bạn
dán hồ sơ vào, bạn nhận lại một con số, bạn đóng tab, và công cụ kết thúc phiên
làm việc với đúng những gì nó biết lúc bắt đầu. Một cuộc tìm việc là bốn mươi
lần nộp đơn trải trên ba tháng. Lần nào cũng trả giá đầy đủ.

## Công cụ này làm gì thay vào đó

**Nó dựng một mô hình về bạn, một lần duy nhất.** `/slushpile:onboard` phỏng vấn
bạn và viết ra ba tệp: một hồ sơ năng lực, một tệp tùy chọn, và một bộ câu
chuyện. Hồ sơ năng lực không phải là một bản CV — nó là cái kho mà mỗi bản CV
được cắt ra từ đó, dài hơn nhiều lần bất cứ thứ gì bạn từng gửi đi. Mọi giai
đoạn về sau đều đọc nó, và không có gì hỏi bạn những câu đó lần thứ hai.

**Nó cố can bạn ra khỏi vị trí đó trước khi bạn viết bất cứ dòng nào.** Giai
đoạn tìm kiếm chấm điểm từng tin tuyển dụng so với nhóm ứng viên ước tính, chạy
các tiêu chí loại thẳng, dựng một ma trận giá trị kỳ vọng cho từng kênh ứng
tuyển, và đặt một người phản biện đứng chắn trước danh sách xếp hạng. Mọi công
cụ khác chỉ bắt đầu làm việc sau khi bạn đã quyết định nộp. Sai lầm đắt đỏ xảy
ra trước thời điểm đó, và đây là giai đoạn duy nhất còn kịp bắt được nó mà không
tốn gì.

**Nó đi mở đúng cái kênh mà chính nó nói là tốt nhất.** Một ma trận định giá
việc giới thiệu cao gấp nhiều lần nộp nguội thì cũng vô nghĩa nếu chẳng ai làm
gì với nó. `/slushpile:outreach` đọc lịch sử của chính bạn để tìm người bạn đã
quen ở đó, hỏi bạn câu hỏi duy nhất mà không tệp nào giữ, chỉ tra cứu người cụ
thể từ hiện diện nghề nghiệp công khai khi bạn không quen ai, rồi soạn lời nhờ
bằng giọng văn của bạn. Nó chấm từng con đường theo điều mà người đó thực sự có
thể nói về công việc của bạn, rồi ghi vào `job_search.md`, đúng chỗ lần đánh giá
kế tiếp đọc để biết kênh ấy có mở hay không. Nó không bao giờ gửi gì cả.

**Nó tấn công chính thứ nó vừa viết.** Một mô hình được hỏi bản nháp của chính
nó có tốt không sẽ trả lời là có, và trả lời rất dài. Nên trình dựng hồ sơ không
hỏi. Nó giao bản CV và lá thư cho 7 người đánh giá, trong đó 5 người đánh giá
song song và không thấy phát hiện của nhau, mỗi người chỉ được đưa đúng những gì
vai trò đó thực sự có trong tay — người sàng lọc mười một giây không bao giờ
được xem thư xin việc, vì một người sàng lọc đã đọc lá thư thì không còn là
người sàng lọc nữa. Trình dựng sửa những gì nhận về và gửi đi đánh giá lại. Vòng
hai phải trụ được thì nó mới cho bạn nộp, và nó dừng ở ba vòng, vì quá đó thì
những khoảng trống là do cấu trúc và sửa thêm chỉ là động tác thừa.

**Nó ghi những gì học được ngược trở lại vào bạn.** Khi một vòng đánh giá nói
một phần nào đó còn mỏng, cuộc phỏng vấn theo sau thường phát hiện ra kinh
nghiệm đó là có thật và bạn chỉ chưa bao giờ viết nó xuống. Điều đó đi vào hồ sơ
năng lực vĩnh viễn. Các ước lượng tỷ lệ chuyển đổi được hiệu chỉnh theo những
kết quả bạn ghi lại. Lần nộp đơn thứ hai mươi của bạn xuất phát từ một chỗ tốt
hơn lần đầu, điều mà ở mọi công cụ khác đơn giản là không đúng.

Thứ đi ra là một phán quyết cho mỗi kênh — nộp nguội, giới thiệu nội bộ, chủ
động liên hệ, được tìm đến nhờ công việc công khai của bạn — mỗi phán quyết kèm
một khoảng xác suất chứ không phải một chữ phán quyết, và chất lượng tài liệu
được chấm tách riêng khỏi giá trị kỳ vọng. "1-3% được phỏng vấn" là thông tin.
"MAYBE" thì không. Tài liệu xuất sắc gửi cho một vị trí không hợp vẫn có giá trị
kỳ vọng thấp, và hai con số đó thường xuyên mâu thuẫn nhau.

## Điều gì thay đổi

Cùng một hồ sơ, cùng một tin tuyển dụng, cùng một buổi chiều.

### Một công cụ tối ưu hồ sơ nói gì với bạn

> **Điểm khớp: 91%** ✅
>
> Tin tốt — hồ sơ của bạn rất khớp với vị trí này!
>
> ✅ Tìm thấy 14 trong 16 từ khóa bắt buộc
> ✅ Phát hiện định dạng thân thiện với ATS
> ⚠️ Cân nhắc bổ sung: "stakeholder alignment", "OKRs"
>
> Bạn sẵn sàng nộp rồi!

### Slushpile nói gì với bạn

> **Vị trí trong nhóm ứng viên: p55.** Ứng viên trung vị ở đây đã triển khai ở
> quy mô tương đương tại một công ty mà quản lý tuyển dụng nhận ra tên. Công
> việc mã nguồn mở của bạn là thật và nó không hiếm trong nhóm này — khoảng một
> phần ba nhóm p75 có thứ tương đương.
>
> **Nộp nguội: REJECT, 1-3%.** Ô chọn số năm kinh nghiệm trên biểu mẫu chặn ở
> mức 8. Bạn có 6 năm ở đúng chức năng mang chức danh đó.
>
> **Giới thiệu nội bộ: MAYBE, 20-30%.** Đây là kênh duy nhất có một con đường
> thật.
>
> **Chất lượng tài liệu: 8/10.** Tài liệu không phải là vấn đề.
>
> **Người phản biện:** SUBMIT_AS_PORTFOLIO_ONLY. Gửi nguội cái này tốn một giờ
> để đổi lấy một cơ hội 2%. Hai giờ đi tìm một lời giới thiệu đáng giá hơn mười
> lần nộp nguội nữa.

Một trong hai thứ đó là một con số về tài liệu của bạn. Thứ còn lại là một quyết
định về buổi chiều của bạn.

## Quy trình

<!-- BEGIN GENERATED pipeline: scripts/sync_docs.py -->

### The main pipeline

Three commands, in order. A search runs on these alone.

```
/slushpile:onboard              once per workspace — builds your profile,
                                preferences, and stories

/slushpile:job-board-search     search a careers board, extract postings,
                                score pool-anchored fit, contrarian gate,
                                create role folders

/slushpile:application-builder  build the resume and cover letter, then
                                iterate them against the review until they
                                stabilize
```

### The three dispatched for you

`/slushpile:application-builder` dispatches `adversarial-review`,
`explore-experience` and `removing-ai-tells`; `/slushpile:outreach` dispatches
`removing-ai-tells`. Run one directly only to work on materials this pipeline
did not build — a resume written elsewhere, a letter drafted by hand.

```
/slushpile:explore-experience   interview to surface experience you have
                                but never wrote down

/slushpile:adversarial-review   seven agents, five in parallel, verdict
                                per channel

/slushpile:removing-ai-tells    strip AI-authorship signals from prose,
                                with a gatekeeper on every change
```

### Any time

```
/slushpile:outreach             find who they already know at the company,
                                grade the path, and draft the ask

/slushpile:redesign-templates   restyle the resume and letter templates,
                                holding the ATS constraints fixed

/slushpile:status               the queue, what is waiting on you, and whether
                                the pipeline's predictions are holding up

/slushpile:help                 what to run next, and how to read the output
```

<!-- END GENERATED pipeline -->

<!-- BEGIN GENERATED reviewers: scripts/sync_docs.py -->

### The seven reviewers

| Agent | Simulates |
|---|---|
| **Triage screener** | 11 seconds, F-pattern, 347 resumes already read today |
| **Requirements analyst** | 30 seconds, methodical, checks every qualification against evidence |
| **ATS simulator** | A parser. Not a reader. Structure, keywords, and years-of-experience math |
| **Fatigued reader** | Application #61 of 80. What annoys, what gets skimmed, what closes the tab |
| **Pool analyst** | A recruiter who knows what the queue actually looks like |
| **Hiring manager** | The person who has to justify the interview slot to their skip-level |
| **Contrarian** | Whoever should have asked whether any of this was worth doing |

The first five run in parallel and cannot see each other's work. The hiring
manager sees all five. The contrarian sees everything, including the hiring
manager, and can overrule it.

<!-- END GENERATED reviewers -->

## Sách hướng dẫn

Phần còn lại nằm ở [docs/](docs/index.md):

- [Bắt đầu](docs/getting-started.md): cần chuẩn bị những gì trước khi onboarding,
  và cần cài những gì.
- [Kỹ năng](docs/skills.md): mọi lệnh, và khi nào thì chạy lệnh nào.
- [Không gian làm việc](docs/workspace.md): những tệp mà công cụ này ghi vào thư
  mục của bạn.
- [Tác nhân giọng văn của bạn](docs/voice.md), [Xử lý sự cố](docs/troubleshooting.md).
- [Kiến trúc](docs/architecture/index.md): các sơ đồ, vì sao vòng đánh giá có
  hình dạng như vậy, và cách chấm điểm và hiệu chỉnh vận hành.

## Thư xin việc của bạn cần giọng văn của bạn

Tác nhân thứ tám viết thư xin việc. Nó viết theo văn phong của một người cụ thể,
dựng lên từ một kho văn bản do chính người đó viết.

slushpile đóng gói sẵn **`aaddrick-voice`** như một ví dụ chạy được để quy trình
hoạt động ngay từ đầu. Đó là giọng văn của tác giả plugin, không phải của bạn.
Những lá thư viết bằng nó sẽ nghe như giọng của một người lạ cụ thể — ổn để xem
quy trình chạy, sai cho bất cứ thứ gì bạn thực sự gửi đi.

Hãy tạo giọng văn của riêng bạn bằng
**[written-voice-replication](https://github.com/aaddrick/written-voice-replication)**.
Nó phân tích một kho văn bản của bạn trên 25 chiều và xuất ra một tác nhân giọng
văn, một kỹ năng giọng văn, và một hồ sơ định lượng với các mục tiêu đo được.
`aaddrick-voice` chính là ví dụ thực hành của quy trình đó.

Rồi trỏ `preferences.yaml` vào nó:

```yaml
voice:
  agent: "your-name-voice"
  is_mine: true
```

Chừng nào `is_mine` còn là false, mọi kỹ năng có soạn văn xuôi đều cảnh báo bạn
trước khi chạy. Cảnh báo đó là thứ duy nhất đứng giữa bạn và mười hai lá đơn gửi
đi bằng giọng của một người lạ.

## Dữ liệu của bạn vẫn là của bạn

`/slushpile:onboard` ghi ba tệp vào thư mục *của bạn*: `profile.md`,
`preferences.yaml`, và `stories.md`. Mọi thông tin cá nhân mà quy trình dùng đều
nằm ở đó. Không có gì bị mã hóa cứng vào plugin, và kho mã có một cổng kiểm tra
CI sẽ báo lỗi nếu một thông tin cá nhân rò rỉ vào một kỹ năng.

Không gian làm việc đó sẽ chứa toàn bộ lịch sử công việc, các con số lương
thưởng, và các ràng buộc của bạn. Hãy giữ nó trong một kho **riêng tư**, hoặc
không đưa vào kho nào cả. Kỹ năng onboarding sẽ nói điều này với bạn và nó sẽ
không tự khởi tạo kho nào cho bạn.

**Quy trình này không bao giờ nộp bất cứ thứ gì.** Không kỹ năng nào chạm vào
một cổng tuyển dụng, một email, hay một biểu mẫu. Nó ghi ra tệp. Bạn đọc chúng
và bạn gửi chúng.

## Sự thẳng thắn chính là tính năng

Công cụ này sẽ nói với bạn rằng một điểm khác biệt bạn tự hào chỉ là mức trung
vị. Nó sẽ nói với bạn rằng một vị trí bạn muốn có tỷ lệ chuyển đổi 2%. Thỉnh
thoảng nó sẽ khuyên bạn đừng nộp.

Đó chính là sản phẩm. Một quy trình chấm phần lớn hồ sơ là INTERVIEW rồi chuyển
đổi được 5% trong số đó không tạo ra tín hiệu, nó tạo ra sự lạc quan, và nó sẽ
làm vậy mãi mãi vì không có gì trong nó phản biện lại. Lượt phản biện, việc neo
theo nhóm ứng viên, và các xác suất theo từng kênh đều tồn tại để đầu ra dùng
được đúng vào lúc nó nói không.

Có một bảng `Calibration` trong tệp theo dõi ở không gian làm việc chính là vì
lý do đó: bạn ghi lại quy trình đã dự đoán gì và thực tế đã xảy ra gì, rồi các
giả định ban đầu được hiệu chỉnh bằng chính lịch sử của bạn thay vì bằng sự tự
tin của bất kỳ ai.

## Tinh chỉnh nó

10 kỹ năng và 8 tác nhân đều là Markdown. Hãy fork, sửa, cài bản của bạn:

```bash
claude plugin uninstall slushpile
```

```bash
claude plugin marketplace remove slushpile
```

```bash
claude plugin marketplace add <your-username>/slushpile
```

```bash
claude plugin install slushpile@slushpile
```

Nếu bạn sửa một kỹ năng, hãy chạy các cổng kiểm tra trước khi push. Xem [CONTRIBUTING.md](../../CONTRIBUTING.md).

## Giấy phép

MIT. Xem [LICENSE](../../LICENSE).
