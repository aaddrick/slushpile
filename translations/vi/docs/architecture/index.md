# Kiến trúc Slushpile

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../../docs/architecture/index.md">English</a> ·
  <a href="../../../zh-CN/docs/architecture/index.md">简体中文</a> ·
  <a href="../../../es/docs/architecture/index.md">Español</a> ·
  <a href="../../../pt-BR/docs/architecture/index.md">Português (BR)</a> ·
  <strong>Tiếng Việt</strong> ·
  <a href="../../../en-x-aibro/docs/architecture/index.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

Slushpile không phải là một chương trình. Nó là một tập hợp các tệp Markdown mà
một tác nhân lập trình đọc rồi hành động theo: 10 kỹ năng làm việc điều phối,
8 định nghĩa tác nhân mà mỗi cái chỉ làm đúng một việc, và một ít mẫu tài liệu.
Không có engine, không có runtime, và không có trạng thái nào nằm ngoài thư mục
không gian làm việc của chính bạn.

Điều đó định hình mọi quyết định được ghi lại ở đây. Một quy tắc mà quy trình
này muốn được thực thi thì phải sống sót qua việc bị một mô hình đang quá tải
diễn đạt lại, vì không có trình thông dịch nào để cưỡng chế nó. Một dữ kiện mà
quy trình cần thì phải nằm trong một tệp mà mô hình thực sự sẽ đọc, vì không có
cơ sở dữ liệu nào để truy vấn.

| Tệp | Nội dung |
| --- | --- |
| [pipeline.md](pipeline.md) | Năm sơ đồ, phần chú giải, và mỗi giai đoạn làm gì. |
| [the-review.md](the-review.md) | Vì sao vòng đánh giá có hình dạng như hiện nay: giai đoạn mù, thứ tự điều phối, người gác cổng, và trần ba vòng. |
| [scoring.md](scoring.md) | Neo theo nhóm ứng viên, phán quyết theo từng kênh, các hạng, và tiêu chí loại. |
| [memory-and-calibration.md](memory-and-calibration.md) | Không gian làm việc như một trí nhớ bền vững, các đường ghi ngược, và cách các dự đoán được kết quả thật sửa lại. |
| [agents-and-models.md](agents-and-models.md) | Ranh giới giữa kỹ năng và tác nhân, mức mô hình cho từng vai, và các tác nhân giọng văn. |
| [personal-data.md](personal-data.md) | Vì sao không một dữ kiện cá nhân nào được phép nằm trong plugin, và cổng chặn cưỡng chế điều đó. |
| [generated-surfaces.md](../../../../docs/architecture/generated-surfaces.md) | Vì sao có sáu bề mặt cùng mô tả quy trình này mà không bề mặt nào sở hữu một dữ kiện. |
| [AGENTS.md](../../../../docs/architecture/AGENTS.md) | Bản sinh đôi giống từng byte của `CLAUDE.md` trong thư mục này, ràng buộc mọi sửa đổi vào các quy ước ở đây. |
