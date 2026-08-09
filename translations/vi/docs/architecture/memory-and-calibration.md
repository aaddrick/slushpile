# Trí nhớ và hiệu chỉnh

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../../docs/architecture/memory-and-calibration.md">English</a> ·
  <a href="../../../zh-CN/docs/architecture/memory-and-calibration.md">简体中文</a> ·
  <a href="../../../es/docs/architecture/memory-and-calibration.md">Español</a> ·
  <a href="../../../pt-BR/docs/architecture/memory-and-calibration.md">Português (BR)</a> ·
  <strong>Tiếng Việt</strong>
</p>

<!-- END GENERATED language-nav -->

Một đợt tìm việc là bốn mươi hồ sơ trải ra trong ba tháng. Một công cụ không có
trí nhớ tính đủ giá cho từng hồ sơ một: bạn dán một bản CV vào, nhận về một con
số, đóng tab lại, và công cụ kết thúc phiên làm việc với đúng những gì nó đã
biết lúc bắt đầu.

Trí nhớ của Slushpile là một thư mục các tệp thuộc về bạn. Không có cơ sở dữ
liệu, không có tài khoản, và không có trạng thái nào bên trong plugin: plugin là
mã nguồn công khai còn không gian làm việc là lịch sử nghề nghiệp của bạn, nên
chúng là hai thứ khác nhau và được để ở hai nơi khác nhau. Xem
[personal-data.md](personal-data.md).

## Cái gì là bền vững

| Tệp | Được ghi bởi | Được đọc bởi |
| --- | --- | --- |
| `profile.md` | `onboard`, được mở rộng bởi `explore-experience` và `application-builder` | mọi giai đoạn có viết văn xuôi |
| `preferences.yaml` | `onboard`, được `status` sửa lại | việc chấm điểm, tiêu chí loại, khâu điều phối của vòng đánh giá |
| `stories.md` | `onboard` | builder, khi nó chọn câu chuyện duy nhất để kể |
| `job_search.md` | `job-board-search`, `application-builder`, `status` | chuyên viên phân tích nhóm ứng viên, người phản biện, hàng đợi |
| `companies.md` | `job-board-search` | các lần tìm kiếm sau tại cùng công ty |
| `applications/<company>/<role>/` | `job-board-search`, rồi tới builder | vòng đánh giá, và `status` |

`profile.md` không phải một bản CV. Nó là kho chất liệu mà một bản CV được cắt
ra từ đó, dài hơn nhiều lần bất cứ thứ gì ai đó sẽ gửi đi, và giá trị của nó là
không bao giờ có thứ gì hỏi bạn những câu đó lần thứ hai.

## Các đường ghi ngược

Có ba đường, và mỗi đường tồn tại vì thứ học được ở một giai đoạn là vô dụng nếu
nó ở lại đó.

**Phát hiện của vòng đánh giá → hồ sơ.** Khi một vòng đánh giá nói rằng một mục
quá mỏng, cuộc phỏng vấn tiếp sau đó thường phát hiện ra trải nghiệm ấy là có
thật và bạn chỉ chưa bao giờ viết nó xuống. `explore-experience` moi nó ra và nó
đi vào `profile.md` vĩnh viễn, nơi mọi hồ sơ về sau đều có thể rút từ đó. Đây là
đường làm cho hồ sơ thứ hai mươi khởi đầu từ một chỗ tốt hơn hồ sơ đầu tiên.

**Kết quả → tệp theo dõi.** Bạn ghi lại chuyện đã xảy ra: không hồi âm, vòng sơ
loại, phỏng vấn, offer, từ chối, và ở giai đoạn nào. Không thứ gì khác trong
quy trình sinh ra được dữ liệu này, vì quy trình không bao giờ nộp bất cứ thứ gì
và không bao giờ nhìn thấy một lời hồi đáp.

**Tệp theo dõi → tiên nghiệm.** `status` hồi quy những gì quy trình đã dự đoán
với các kết quả đó rồi ghi phần hiệu chỉnh vào `preferences.yaml`.

## Vì sao phần hiệu chỉnh đi vào dữ liệu của người dùng

Chỗ hiển nhiên để ghi lại “quy trình này lạc quan hơn 12 điểm về các lần nộp
nguội vào những phòng lab tiên phong” là ở chính tác nhân đã đưa ra ước lượng
đó. Đó là chỗ sai, và sai một cách lặng lẽ: định nghĩa tác nhân được phát hành
kèm plugin, nên một sửa đổi ở đó sẽ bị bản cập nhật kế tiếp hoàn tác mà không
báo trước, để lại một quy trình *từng* được tinh chỉnh và nay thì không.

Nên phần hiệu chỉnh đi vào `preferences.yaml`, tệp thuộc về bạn và không bản cập
nhật nào đụng tới. `job-board-search` đọc `calibration_priors` lúc chấm điểm, và
`adversarial-review` truyền khối đó cho chuyên viên phân tích nhóm ứng viên cùng
người phản biện lúc điều phối.

## Những quy tắc giữ cho việc hiệu chỉnh trung thực

**Năm hồ sơ đã ngã ngũ là sàn.** Dưới mức đó, `status` in ra các con số đếm và
nói rằng mẫu quá nhỏ để hồi quy, thay vì cho ra một cái bảng. Một tỷ lệ tính từ
hai kết quả là nhiễu khoác áo hiệu chỉnh, và một khi nó đã nằm trong bảng thì
không ai còn nhớ mẫu số nữa.

**Im lặng được tính là từ chối.** Một hồ sơ nộp hơn 30 ngày trước mà không có
hồi âm được ghi là `no_response`, chứ không để treo. Loại những hồ sơ đó ra là
nguồn lạc quan lớn nhất có sẵn cho một cái bảng kiểu này. Số lượng suy ra theo
cách đó cũng được báo cáo.

**Chấm theo đúng cái kênh đã dùng.** Các phán quyết được nhóm theo phán quyết
của kênh mà hồ sơ thực sự đi qua, không bao giờ theo kênh tốt nhất. Chấm một lần
nộp nguội theo phán quyết dành cho giới thiệu nội bộ là cách một quy trình tự
thuyết phục mình rằng nó đã đúng.

**Cả hai chiều sai đều được báo cáo.** Một phán quyết INTERVIEW mà bị tự động từ
chối trong vòng 72 giờ nghĩa là vòng đánh giá đã bỏ sót thứ mà một bộ lọc bắt
được trong vài giây. Một phán quyết REJECT mà lại chuyển đổi nghĩa là vòng đánh
giá đã quá khắt khe, và mọi vị trí mà nó can bạn đừng nộp kể từ đó là một cái
giá không hiện ra ở bất cứ đâu khác. Chỉ một trong hai chiều đó là dễ chịu để
báo cáo, và đó là lý do quy tắc này gọi tên cả hai.

**Phát hiện phải nêu tên một phân khúc, một chiều, và một độ lớn.** “Quy trình
bị lệch hiệu chỉnh” là câu không hành động được và không tác nhân nào tiêu thụ
được nó. “Các phán quyết INTERVIEW cho lần nộp nguội vào những phòng lab tiên
phong đã chuyển đổi 0 trên 7, so với mức ước lượng 12%” thì có thể được ghi
thành một tiên nghiệm và đem ra hành động.

**Một tiên nghiệm rỗng là một câu trả lời hợp lệ.** Chỉ những tỷ lệ được chống
đỡ bởi từ năm hồ sơ đã ngã ngũ trở lên trên kênh đó mới được ghi. Mọi thứ khác ở
lại trạng thái rỗng, các tác nhân dùng mặc định đi kèm bản phát hành, và chúng
gắn nhãn ước lượng là chưa hiệu chỉnh. Một tiên nghiệm tính từ hai kết quả đẩy
việc chấm điểm xa thực tế hơn là không có tiên nghiệm nào, và nó lại tới với uy
thế của một con số thực nghiệm.

**Bản khác biệt được đưa ra xem trước khi `preferences.yaml` được ghi.** Đó là
tệp ràng buộc của bạn và thay đổi ở đó làm biến đổi cách mọi đánh giá tương lai
chấm điểm. Một thay đổi về chấm điểm mà không ai được báo thì không phân biệt
được với việc quy trình tự trôi đi.
