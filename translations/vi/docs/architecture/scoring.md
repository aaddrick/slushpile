# Chấm điểm

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../../docs/architecture/scoring.md">English</a> ·
  <a href="../../../zh-CN/docs/architecture/scoring.md">简体中文</a> ·
  <a href="../../../es/docs/architecture/scoring.md">Español</a> ·
  <a href="../../../pt-BR/docs/architecture/scoring.md">Português (BR)</a> ·
  <strong>Tiếng Việt</strong> ·
  <a href="../../../en-x-aibro/docs/architecture/scoring.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

Mọi con số mà quy trình này sinh ra đều là câu trả lời cho một trong hai câu
hỏi: ứng viên đứng ở đâu trong hàng đợi cho đúng vị trí này, và một hồ sơ đi qua
một kênh nhất định thực sự đáng giá bao nhiêu. Không có gì ở đây chấm một tài
liệu với một tin tuyển dụng một cách biệt lập, vì đó là một con số thật cho câu
hỏi sai.

## Neo theo nhóm ứng viên

Một điểm khớp từ khóa đem so một bản CV với một mô tả công việc. Không ai được
tuyển bởi một bản mô tả công việc. Phép so quyết định kết quả là phép so với
những ứng viên khác trong hàng đợi, và một điểm khớp thì không nhìn thấy họ.

Nên giai đoạn tìm kiếm ước lượng nhóm ứng viên trước: còn ai khác nộp vào vị trí
này, và ứng viên ở trung vị, ở phân vị 75, ở phân vị 90 trông ra sao. Ứng viên
sau đó được định vị trong phân bố ấy, và **phân vị trong nhóm ứng viên được ghi
lại làm con số phù hợp chính thức.** Điểm khớp từ khóa, nếu vẫn muốn có, được
đặt vào một trường riêng. Gộp hai thứ đó lại chính là kiểu hỏng mà thang chấm
này tồn tại để ngăn.

| Vị trí trong nhóm | Hạng | Nghĩa |
| --- | --- | --- |
| p75+ | Hạng 1 | Trên vạch ứng viên mạnh cho đúng vị trí này |
| p55–p74 | Hạng 2 | Cạnh tranh được, nhưng không có gì khác biệt. Cần một lợi thế về kênh. |
| p35–p54 | Hạng 3 | Dưới trung vị. Chỉ theo đuổi qua một kênh mạnh. |
| dưới p35 | Bỏ qua | Nhóm ứng viên vượt trội hơn hẳn. Một lần nộp nguội là một suất bị phí. |

Các đầu vào được xếp theo thứ tự. Từ hai điều kiện tối thiểu thiết yếu không đạt
trở lên sẽ kéo vị trí xuống một đến hai hạng bất kể mọi thứ khác. Rồi tới phép
so với nhóm ứng viên: tuyên bố mạnh nhất có thực sự xếp cao ở đây không, hay chỉ
là trung vị? Rồi tới độ lệch so với nhịp vận hành thật của vị trí, rồi tới các
yếu tố rủi ro, mỗi yếu tố khoảng năm đến mười điểm phân vị, rồi tới tiên nghiệm
hiệu chỉnh cho công ty đó.

Đầu ra hữu ích nhất của giai đoạn này là một điểm khác biệt mà ứng viên tự nhận
lại quay về với nhãn ngang trung vị của nhóm. Đó là thông tin ứng viên không thể
lấy được từ một máy quét tài liệu, và thường là thứ làm thay đổi những gì họ
viết.

## Phán quyết theo từng kênh

Cùng một bộ tài liệu chuyển đổi ở những tỷ lệ rất khác nhau tùy theo cách nó tới
nơi. Một phán quyết duy nhất lấy trung bình trên khác biệt đó rồi báo cáo cái
trung bình như thể nó là một dữ kiện về hồ sơ.

Nên mọi vị trí Hạng 1 đến 3 đều nhận một ma trận thay vì một phán quyết:

| Kênh | Điều kiện chặn | Khoảng qua vòng sơ loại, ước chừng |
| --- | --- | --- |
| Nộp nguội | không có | 5–15%, thay đổi theo vị trí trong nhóm |
| Giới thiệu nội bộ | phải có người giới thiệu | 25–50%, tùy nhóm ứng viên |
| Chủ động liên hệ một nhân viên cụ thể | có một người nhận diện được | 5–15% |
| Thu hút tự nhiên từ công việc công khai | có sẵn một sản phẩm, đã gieo ra | 20–40% nếu nó trúng |
| Recruiter chủ động tìm đến | ngoài tầm kiểm soát của ứng viên | không ước lượng |

Có hai quy tắc giữ cho cái này khỏi trở thành đồ trang trí.

**Hạng của vị trí là hạng cao nhất trên các kênh *có sẵn***, và ma trận ghi lại
kênh nào mở ra hạng đó cùng điều kiện nào phải vượt qua. Nếu hiện chưa có người
giới thiệu nào, dòng giới thiệu nội bộ chỉ mang tính tham khảo và không mở ra
Hạng 1. Thổi phồng một hạng bằng cách dựa vào một kênh không có sẵn là cách phổ
biến nhất khiến ma trận này bị lách, và đó là tự mình gây ra.

**Lịch sử của chính bạn thắng mọi tiên nghiệm.** Ở đâu `job_search.md` ghi lại
một tỷ lệ giới thiệu nội bộ thật tại công ty này, con số đó được dùng thay cho
con số chung. Xem [memory-and-calibration.md](memory-and-calibration.md).

## Chất lượng tài liệu không phải là giá trị kỳ vọng

Vòng đánh giá báo cáo hai thứ này thành hai con số tách biệt vì chúng thường
xuyên không khớp nhau. Tài liệu xuất sắc gửi tới một vị trí không hợp thì vẫn có
giá trị kỳ vọng thấp; tài liệu vừa đủ gửi qua một lời giới thiệu tới một vị trí
hợp thì có giá trị kỳ vọng cao.

Gộp chúng lại là bảo bạn bỏ thêm một tiếng nữa để sửa chữ, trong khi khuyến nghị
trung thực là bỏ tiếng đó đi tìm một người giới thiệu. Điểm tài liệu 8/10 nằm
cạnh tỷ lệ chuyển đổi khi nộp nguội 1–3% không phải là một mâu thuẫn, nó chính
là toàn bộ phát hiện.

## Tiêu chí loại

Tiêu chí loại chạy ngay lúc quét và được đối chiếu với `preferences.yaml`:
lương, địa điểm, quyền truy cập thông tin mật, và bất cứ thứ gì khác bạn đã ghi
lại như một ràng buộc.

Có hai tính chất quan trọng hơn bản thân danh sách.

**Những lượt đạt cũng được nêu, không chỉ những lượt trượt.** Một lượt kiểm tra
chỉ báo cáo cái đã trượt thì không thể phân biệt với một lượt kiểm tra chưa từng
chạy, và ở đây không có trình thông dịch nào để chứng minh là nó đã chạy.

**Một lần bỏ qua phải nêu tên đúng một rào cản chính.** Nếu không rào cản nào tự
nó đủ để biện minh cho việc bỏ qua vị trí đó, thì vị trí đó nhận một điểm số chứ
không phải một lần bỏ qua. Một lần bỏ qua được biện minh bằng cách tích lũy
những nghi ngờ vụn vặt chỉ là một tâm trạng, và nó sẽ không sống sót khi chính
bạn đọc lại một tuần sau.

Lương được đánh giá trên **dải lương đã đăng**, theo phương pháp đã ghi trong
`preferences.yaml`. Các điều khoản ở giai đoạn nhận offer được nói rõ là nằm
ngoài phạm vi ở đây, vì đúng cái lý do chúng bị gạch bỏ trong vòng đánh giá:
xem [the-review.md](the-review.md#the-gatekeeper).

## Khoảng xác suất, không phải chữ phán quyết

Đầu ra là “1–3% được phỏng vấn” chứ không phải “MAYBE”. Một khoảng mang theo độ
bất định của chính nó và có thể đem đối chiếu với chuyện đã thực sự xảy ra; một
chữ phán quyết chẳng mang theo thứ nào và không đối chiếu được.

Đây cũng là thứ làm cho vòng lặp hiệu chỉnh trở nên khả thi. “MAYBE” không thể
đem hồi quy với kết quả. Một tỷ lệ phần trăm thì có thể, và
[memory-and-calibration.md](memory-and-calibration.md) là nơi phép hồi quy đó
diễn ra.
