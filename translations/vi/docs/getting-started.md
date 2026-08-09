# Bắt đầu

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../docs/getting-started.md">English</a> ·
  <a href="../../zh-CN/docs/getting-started.md">简体中文</a> ·
  <a href="../../es/docs/getting-started.md">Español</a> ·
  <a href="../../pt-BR/docs/getting-started.md">Português (BR)</a> ·
  <strong>Tiếng Việt</strong> ·
  <a href="../../en-x-aibro/docs/getting-started.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

Mọi thứ bạn cần trước lần chạy đầu tiên: cài gì, gom gì, và chạy ở đâu.

## Lấy plugin

[INSTALL.md](../INSTALL.md) có một cách cài cho mỗi harness — Claude Code,
Codex, Gemini CLI, Cursor, và một đoạn dán sẵn cho mọi thứ còn lại. Bản rút gọn
cho Claude Code:

```bash
claude plugin marketplace add aaddrick/slushpile
claude plugin install slushpile@slushpile
```

Rồi, trong thư mục nơi bạn muốn đặt quá trình tìm việc của mình:

```
/slushpile:onboard
```

**Hãy chạy nó ở nơi khác với bản checkout của plugin.** Plugin là mã nguồn công
khai. Không gian làm việc là lịch sử việc làm, các con số lương thưởng và các
ràng buộc của bạn. Xem [Không gian làm việc](workspace.md).

## Onboarding sẽ hỏi bạn những gì

Đáng gom trước khi bắt đầu, vì hai trong số này ngốn của bạn nhiều thời gian
tìm hơn cả thời gian chạy hết cuộc phỏng vấn.

**Một bản CV**, ở định dạng bất kỳ. PDF, `.tex`, `.docx`, Markdown. Nó thay
khoảng mười phút phỏng vấn bằng ba mươi giây đọc. Bản xuất dữ liệu LinkedIn
cũng dùng được — `Positions.csv` và `Education.csv` chứa phần lớn nội dung đó.

**Một kho văn bản của bạn**, dành cho tác nhân giọng văn. Vài nghìn từ văn xuôi
do chính bạn viết và chưa qua biên tập. Onboarding không tự phân tích kho này —
nó chỉ bạn sang
[written-voice-replication](https://github.com/aaddrick/written-voice-replication),
một quy trình riêng mà bạn chạy một lần. Gom kho văn bản mới là phần chậm, nên
hãy bắt đầu sớm. Xem [Tác nhân giọng văn của bạn](voice.md).

Nguồn tốt: bài trên diễn đàn và Reddit, bài blog, tin nhắn Slack dài, email gửi
đồng nghiệp, mô tả pull request, tài liệu bạn viết một mình. Bản xuất dữ liệu
Reddit hoặc Twitter dùng được ngay.

Nguồn tệ: bất cứ thứ gì viết chung, bất cứ thứ gì người khác biên tập, bất cứ
thứ gì đã chạy qua một LLM, bất cứ thứ gì mang giọng của tổ chức. Copy quảng
cáo và bản đánh giá hiệu suất là hai thứ tệ nhất.

**Các con số của bạn.** Ngân sách, quy mô nhân sự, phần trăm, và trạng thái
*trước đó* của từng thứ. "Cắt độ trễ 40%" là vô dụng chừng nào chưa biết 40%
của cái gì, và onboarding sẽ hỏi.

**Tình hình lương thưởng của bạn**, nếu bạn muốn cổng lọc lương hoạt động. Với
phương pháp được khuyến nghị, nó cần thu nhập gộp hiện tại, thuế và chi phí nhà
ở của bạn. Nó tự làm phép tính; bạn không cần mang sẵn một con số.

## Yêu cầu

**Bắt buộc:** một tác nhân đọc được tệp cục bộ và duyệt được web.

**Khuyến nghị:** `pdftotext` (từ `poppler-utils`), để các tác nhân đánh giá nhìn
thấy đúng thứ một ATS nhìn thấy, chứ không phải thứ trình xem PDF của bạn hiển
thị.

```bash
sudo dnf install poppler-utils     # Fedora
sudo apt install poppler-utils     # Debian, Ubuntu
brew install poppler               # macOS
```

**Tùy chọn:** một bộ công cụ LaTeX, nếu bạn dùng `templates/resume.tex` và
`templates/cover_letter.tex`. Mọi kỹ năng đều làm việc trên văn bản đã trích
xuất và không kỹ năng nào cần LaTeX — chỉ hai mẫu tài liệu đó cần.

```bash
sudo dnf install -y texlive-xetex texlive-fontspec texlive-microtype latexmk dejavu-fonts-all
sudo apt install texlive-xetex texlive-fonts-extra fonts-dejavu latexmk
brew install --cask mactex-no-gui
```

Dựng bằng `latexmk -xelatex resume.tex && latexmk -c`. Hai lệnh: lệnh đầu dựng,
lệnh sau dọn. Không lệnh nào làm cả hai.

Hai mẫu tài liệu được trình bày bằng Public Sans và IBM Plex Mono. Không phông
nào đi kèm TeX Live, nên cả hai đều được đóng gói sẵn trong kho lưu trữ này và
một lệnh sẽ cài chúng:

```bash
python3 scripts/install_fonts.py            # install
python3 scripts/install_fonts.py --check    # report, change nothing
python3 scripts/install_fonts.py --uninstall
```

Nó chép bảy tệp phông vào thư mục phông của người dùng và làm mới bộ nhớ đệm.
Không thứ gì khác chạy nó, và bỏ qua cũng không sao: cả hai mẫu đều lùi về
DejaVu khi thiếu một họ phông, nên phông thiếu chỉ đổi việc tài liệu trông ra
sao chứ không bao giờ đổi việc tài liệu có dựng được hay không.

Để đổi kiểu chúng thành thứ của riêng bạn, hãy chạy
`/slushpile:redesign-templates` thay vì sửa bản checkout của plugin, vì bản cập
nhật kế tiếp sẽ ghi đè lên đó.

## Giờ đầu tiên của bạn

```
/slushpile:onboard                          # once, in your workspace directory
/slushpile:job-board-search <company|query> # search, score, and create role folders
/slushpile:application-builder <path>       # build and review one application
```

`onboard` là một cuộc phỏng vấn chứ không phải một biểu mẫu, và nó là chặng duy
nhất hỏi bạn những câu bạn sẽ không bị hỏi lại. Mọi chặng sau nó đều đọc thứ nó
đã ghi.

Hãy bắt đầu bằng `job-board-search` trên một công ty bạn thật sự quan tâm, chứ
không phải trên vị trí đầu tiên bạn bắt gặp. Chặng tìm kiếm là chặng duy nhất
còn có thể can bạn khỏi một lần ứng tuyển mà không tốn gì, và đó là nơi quy
trình trả lại nhiều nhất trên mỗi phút bạn bỏ ra.

Nếu bạn chưa nhắm sẵn công ty nào, hãy mô tả thứ bạn đang tìm và chính lệnh đó
sẽ phân giải nó thành một danh sách: `applied AI roles within 50 miles of
Martinsville, VA that fit my profile` dùng làm tham số được. Nó cho bạn xem
những công ty nó đã chọn trước khi tìm bất kỳ công ty nào trong số đó, nên một
danh sách dựng trên cách đọc sai truy vấn của bạn chỉ tốn của bạn một lần đính
chính chứ không phải một tiếng đồng hồ.

[Kỹ năng](skills.md) là tài liệu tra cứu đầy đủ về các lệnh.
