# Xử lý sự cố

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../docs/troubleshooting.md">English</a> ·
  <a href="../../zh-CN/docs/troubleshooting.md">简体中文</a> ·
  <a href="../../es/docs/troubleshooting.md">Español</a> ·
  <a href="../../pt-BR/docs/troubleshooting.md">Português (BR)</a> ·
  <strong>Tiếng Việt</strong> ·
  <a href="../../en-x-aibro/docs/troubleshooting.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

**`plugin install` chạy xong nhưng các kỹ năng không hiện ra.** Chạy
`claude plugin list` và kiểm tra xem có `enabled` không. Kỹ năng chỉ được nạp
lúc phiên bắt đầu, nên hãy mở một phiên mới hoặc chạy `/clear`.

**Một kỹ năng báo rằng nó không tìm thấy `preferences.yaml`.** Bạn đang ở một thư
mục khác với thư mục bạn đã chạy onboarding. Mọi kỹ năng đều đọc không gian làm
việc từ thư mục làm việc hiện tại. Xem [Không gian làm việc](workspace.md).

**Các tác nhân đánh giá báo rằng CV gần như trống rỗng.** Chúng đang đọc phần văn
bản trích xuất được, không phải bản PDF như bạn nhìn thấy. Chạy
`pdftotext yourresume.pdf -` rồi nhìn vào kết quả. Nếu nó trống hoặc lộn xộn thì
CV có vấn đề về bố cục (lưới nhiều cột, một hộp văn bản, thông tin liên hệ nằm
trong phần đầu trang) và đó là một phát hiện thật, không phải lỗi công cụ. Một hệ
thống ATS nhìn thấy đúng những gì `pdftotext` nhìn thấy.

**Thư xin việc đọc lên nhàn nhạt chung chung, hoặc nghe như của người khác.** Kiểm
tra `voice.is_mine` trong `preferences.yaml`. Nếu nó là false thì bạn đang dùng
giọng ví dụ đi kèm, vốn thuộc về tác giả plugin. Hãy tự sinh giọng của riêng bạn
bằng
[written-voice-replication](https://github.com/aaddrick/written-voice-replication)
rồi trỏ `voice.agent` vào đó. Nếu nó đã là true thì nhiều khả năng kho văn bản
còn quá mỏng: vài nghìn từ là mức sàn. Xem
[Tác nhân giọng văn của bạn](voice.md).

**Vai trò nào cũng bị loại thẳng vì lương thưởng.** Mở `preferences.yaml` và kiểm
tra `compensation`. Với `net_qol`, nguyên nhân thường gặp nhất là
`current_baseline` được nhập theo lương gộp thay vì theo mức sau thuế và sau chi
phí nhà ở, khiến mọi lời mời đều trông tệ hơn thực tế.

**Vai trò nào cũng ra Hạng 1.** Có thứ gì đó đang chấm điểm dựa trên tin tuyển
dụng chứ không dựa trên nhóm ứng viên. Kiểm tra xem `role_analysis.md` có thực sự
chứa các mẫu hình theo phân vị cho vai trò đó không, chứ không chỉ là một phép so
sánh từ khóa: một điểm phù hợp không có ước lượng nhóm ứng viên đứng sau chỉ là
một điểm so khớp đội lốt phân vị. Xem [Chấm điểm](architecture/scoring.md).

**Vòng đánh giá không bao giờ nói không.** Kiểm tra xem người phản biện có chạy
hay không: phán quyết ròng của nó phải xuất hiện trong bản tóm tắt của quy trình
và trong `application.yaml` dưới `contrarian_net`. Nó được thiết kế để chạy tự
động chứ không phải có điều kiện, và một vòng đánh giá thiếu nó là một vòng đánh
giá không có bước phản chứng.

**Phần hiệu chỉnh nói rằng chưa đủ dữ liệu, trong khi rõ ràng là đã đủ.** Mức sàn
là năm bộ hồ sơ *đã ngã ngũ*, và một bộ hồ sơ chỉ được tính là đã ngã ngũ khi
`outcome.stage_reached` được điền, hoặc khi nó đã nộp hơn 30 ngày trước mà không
có hồi âm. Những bộ hồ sơ nằm trong `application.yaml` với phần kết quả để trống
được tính là đang treo, chứ không phải là bị từ chối. `/slushpile:status` báo cho
bạn biết bản ghi nào còn thiếu.

**Một vòng đánh giá cho ra đúng những phát hiện như vòng trước.** Đó chính là tín
hiệu, không phải lỗi. Một vấn đề bị gắn cờ ở nhiều hơn một vòng là vấn đề thật;
một vấn đề chỉ bị gắn cờ một lần là nhiễu. Nếu đến vòng thứ ba mà không có gì
dịch chuyển thì những khoảng trống đó là mang tính cấu trúc, và quy trình được
thiết kế để nói thẳng như vậy thay vì chạy vòng thứ tư.

**Quy trình sẽ không nộp hồ sơ thay bạn.** Nó sẽ không bao giờ làm thế. Không kỹ
năng nào chạm vào một cổng tuyển dụng, một email, hay một biểu mẫu. Nó ghi ra các
tệp; bạn đọc chúng và bạn gửi chúng.
