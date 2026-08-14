# Các kỹ năng

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../docs/skills.md">English</a> ·
  <a href="../../zh-CN/docs/skills.md">简体中文</a> ·
  <a href="../../es/docs/skills.md">Español</a> ·
  <a href="../../pt-BR/docs/skills.md">Português (BR)</a> ·
  <strong>Tiếng Việt</strong> ·
  <a href="../../en-x-aibro/docs/skills.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

Slushpile cài đặt vào máy dưới dạng 10 kỹ năng. Claude Code hiện mỗi kỹ năng ra
thành `/slushpile:<name>`; Codex dùng `$slushpile:<name>`; Gemini CLI và các
harness khác đọc chính những tệp đó, và bạn gọi tên giai đoạn bằng lời.

Ba trong số đó là xương sống. Ba kỹ năng nữa được điều phối sẵn cho bạn trong lúc
dựng một bộ hồ sơ, và bạn chỉ chạy tay chúng trên tài liệu mà quy trình này không
dựng ra. Bốn kỹ năng cuối bạn chạy khi chúng dùng được, theo thứ tự nào cũng
được.

## Xương sống

### `/slushpile:onboard`

Dựng không gian làm việc. Nạp một CV sẵn có hoặc bản xuất dữ liệu LinkedIn, phỏng
vấn bạn để lấp những chỗ còn trống, rồi ghi ra `profile.md`, `preferences.yaml`
và `stories.md`. Kiểm tra bộ công cụ dựng tài liệu, dựng khung cho tệp theo dõi,
rồi bàn giao.

Chạy một lần cho mỗi không gian làm việc, trước mọi thứ khác. Xem
[Bắt đầu](getting-started.md) để biết cần chuẩn bị sẵn những gì, và
[Không gian làm việc](workspace.md) để biết nó ghi ra những gì.

### `/slushpile:job-board-search`

Tìm trên một trang tuyển dụng, trích nguyên văn từng tin tuyển dụng, ước lượng
nhóm ứng viên thực tế, chấm độ phù hợp neo theo nhóm ứng viên và theo từng kênh,
chạy các tiêu chí loại thẳng, đặt một người phản biện chắn trước danh sách phân
hạng, rồi tạo một thư mục vai trò cho mỗi vai trò còn sống sót.

**Tham số:** tên một công ty, hoặc một truy vấn mô tả công việc bạn muốn làm và
nơi bạn muốn làm nó. Khi nhận một truy vấn, Giai đoạn 0 phân giải nó thành một
danh sách công ty, đọc các ràng buộc của bạn từ `preferences.yaml` và lịch sử
của bạn từ `companies.md`, đưa danh sách đó cho bạn xem, rồi mới tìm sau khi bạn
xác nhận. Mọi thứ sau Giai đoạn 0 đều như nhau ở cả hai đường, nên một bản đánh
giá từ lần chạy bằng truy vấn vẫn so sánh được với một bản từ lần chạy nêu đích
danh công ty, và bảng hiệu chỉnh có thể gộp chung chúng lại.

Đây là giai đoạn cho lợi ích cao nhất trong quy trình, và là giai đoạn hầu hết
công cụ khác không có. Mọi thứ đứng sau nó tốn một buổi chiều cho mỗi bộ hồ sơ;
giai đoạn này tốn vài phút và có thể kết thúc bằng "không vai trò nào cả". Xem
[Chấm điểm](architecture/scoring.md).

### `/slushpile:application-builder`

Dựng CV và thư xin việc nhắm riêng cho một thư mục vai trò đã có sẵn mô tả công
việc và bản phân tích vai trò, rồi lặp chúng qua vòng đánh giá cho tới khi chúng
ổn định hoặc chạm trần ba vòng.

**Tham số:** đường dẫn tới một thư mục vai trò.

Nó tự điều phối `explore-experience`, `adversarial-review` và
`removing-ai-tells`. Nó không bao giờ nộp bất cứ thứ gì; nó giao cho bạn những
tệp đã hoàn chỉnh.

## Ba kỹ năng được điều phối sẵn cho bạn

Chỉ chạy trực tiếp một trong số này khi bạn cần xử lý tài liệu mà quy trình này
không dựng ra: một CV viết ở nơi khác, một lá thư soạn tay.

### `/slushpile:adversarial-review`

Chạy 7 người đánh giá lên một CV và một thư xin việc. Trả về một phán quyết và
một khoảng xác suất cho từng kênh nộp, chất lượng tài liệu được chấm tách khỏi
giá trị kỳ vọng, và một lượt phản biện có thể lật ngược tất cả phần còn lại.

**Tham số:** đường dẫn tới một thư mục vai trò chứa tối thiểu một CV và
`job_description.md`.

Xem [Vòng đánh giá](architecture/the-review.md) để biết mỗi người đánh giá được
cho xem những gì, và bị giấu những gì một cách có chủ đích.

### `/slushpile:explore-experience`

Phỏng vấn bạn để lôi ra thứ kinh nghiệm có thật nhưng chưa từng được ghi lại, đối
chiếu với yêu cầu của một vai trò cụ thể, rồi ghi nó vĩnh viễn vào `profile.md`.

Dùng khi một bản đánh giá độ phù hợp hoặc một vòng đánh giá gắn cờ rằng một mục
còn mỏng. Phần lớn thời gian, kinh nghiệm đó hóa ra là có thật và chỉ đơn giản là
chưa bao giờ được viết ra, đó là lý do đây là một cuộc phỏng vấn chứ không phải
một lần viết lại.

### `/slushpile:removing-ai-tells`

Gỡ bỏ những cách diễn đạt, cấu trúc và lựa chọn từ ngữ để lộ dấu vết AI, chạy
nhiều lượt lặp qua các phiên bản mới tinh của tác nhân giọng văn, với bộ điều
phối gác cổng từng thay đổi một.

Dùng cho một thư xin việc trước khi nộp, hoặc cho bất kỳ đoạn văn nào buộc phải
đọc lên như do người viết.

## Bất cứ lúc nào

### `/slushpile:outreach`

Mở kênh ấm cho một vị trí. Nó đọc bảng giới thiệu và hồ sơ của bạn để tìm những
người bạn đã quen ở công ty đó, hỏi bạn câu hỏi mà không tệp nào trả lời được,
chỉ tra cứu người cụ thể từ hiện diện nghề nghiệp công khai khi bạn không quen
ai, chấm điểm từng con đường theo điều mà người đó thực sự có thể nói về công
việc của bạn, rồi soạn lời nhờ giới thiệu hoặc thư lạnh bằng tác nhân giọng văn
của bạn.

**Tham số:** đường dẫn tới một thư mục vị trí.

Chạy nó khi bản đánh giá nói rằng giới thiệu chuyển đổi cao gấp nhiều lần nộp
lạnh mà bạn lại chưa có ai giới thiệu. Không có bước này, quy trình tính ra kênh
tốt nhất của bạn là giới thiệu, nói cho bạn biết điều đó, rồi vẫn dựng tài liệu
cho cổng nộp lạnh. Nó ghi các đầu mối vào `job_search.md`, đúng chỗ vòng đánh
giá đọc chúng: chừng nào dòng đó chưa tồn tại, mọi lượt đánh giá của mọi vị trí ở
công ty đó đều coi kênh ấm là không có sẵn, và coi vậy là đúng.

Nó không bao giờ gửi gì cả. Tin nhắn là của bạn, gửi từ tài khoản của bạn.

### `/slushpile:redesign-templates`

Đổi phong cách `resume.tex` và `cover_letter.tex` sang phong cách riêng của bạn
(kiểu chữ, bảng màu, bố cục) trong khi vẫn giữ nguyên các ràng buộc ATS, rồi
chứng minh rằng kết quả vẫn biên dịch được và vẫn trích xuất được văn bản.

Chạy kỹ năng này thay vì sửa thẳng vào bản checkout của plugin, thứ mà bản cập
nhật kế tiếp sẽ thay thế.

### `/slushpile:status`

Đọc mọi `application.yaml` trong không gian làm việc và báo cáo tình trạng cuộc
tìm việc: hàng đợi đã xếp hạng, thứ đang chờ bạn, thứ đã im lặng, và phép hồi quy
giữa chính dự đoán của quy trình với những gì thực sự đã xảy ra. Ghi các kết quả
hiệu chỉnh trở lại vào `job_search.md` và `preferences.yaml`.

Chạy nó sau khi kết quả đã về. Xem
[Trí nhớ và hiệu chỉnh](architecture/memory-and-calibration.md).

### `/slushpile:help`

Giải thích slushpile là gì, mỗi kỹ năng làm gì, chạy chúng theo thứ tự nào, các
tệp của không gian làm việc nằm ở đâu, và cách thiết lập một tác nhân giọng văn.

Chạy nó khi bạn không chắc mình nên chạy cái gì.
