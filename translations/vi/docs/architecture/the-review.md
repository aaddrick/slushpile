# Vòng đánh giá

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../../docs/architecture/the-review.md">English</a> ·
  <a href="../../../zh-CN/docs/architecture/the-review.md">简体中文</a> ·
  <a href="../../../es/docs/architecture/the-review.md">Español</a> ·
  <a href="../../../pt-BR/docs/architecture/the-review.md">Português (BR)</a> ·
  <strong>Tiếng Việt</strong>
</p>

<!-- END GENERATED language-nav -->

`/slushpile:adversarial-review` điều phối 7 người đánh giá tới tấn công một bản
CV và một lá thư xin việc. Trang này nói vì sao nó có hình dạng đó. Bức tranh
nằm ở [pipeline.md](pipeline.md); định nghĩa của từng tác nhân nằm trong
`agents/`.

## Bốn kiểu hỏng, bốn giai đoạn

Hình dạng này không phải một hội đồng tùy tiện. Mỗi giai đoạn trả lời một cách
cụ thể mà một quy trình đánh giá ngây thơ sinh ra thứ vô nghĩa đầy tự tin.

**Nịnh bợ vì chỉ có một góc nhìn.** Trong một quy trình ngây thơ, mọi người
đánh giá đều làm việc cho ứng viên. Không ai mô hình hóa hàng đợi. Chuyên viên
phân tích nhóm ứng viên tồn tại để ép ra lập luận so sánh: không phải “tài liệu
này có tốt không” mà là “nó có tốt hơn bảy mươi hồ sơ khác mà vị trí này nhận
được trong tuần này không”.

**Phán quyết sụp thành một.** Một câu trả lời duy nhất INTERVIEW / MAYBE / PASS
che mất chuyện cùng bộ tài liệu ấy chuyển đổi ở những tỷ lệ rất khác nhau khi
nộp nguội và khi qua giới thiệu nội bộ. Đó là hai quyết định khác nhau về buổi
chiều của bạn. Quản lý tuyển dụng cho ra một phán quyết trên mỗi kênh, kèm một
khoảng xác suất chứ không phải một từ.

**Nỗi lo phát hiện AI được dựng lên.** Một vai chuyên phát hiện AI sẽ gắn cờ các
mẫu hình dựa trên nghi ngờ giả định của người đọc, và nó sẽ lấn át những phán
đoán có cơ sở về thứ mà một người đọc thật sự để ý. Nó được thay bằng người đọc
mệt mỏi, vai này hỏi một câu trả lời được: cái này có làm phiền một người đang ở
hồ sơ thứ sáu mươi mốt trong ngày không?

**Không có bước phản nghiệm.** Trong một vòng đánh giá bình thường, không có gì
hỏi rằng điều gì phải đúng thì cả bài tập này mới là một sự phí phạm. Người phản
biện hỏi câu đó, hỏi sau cùng, và có quyền lật ngược mọi thứ ở phía trên.

## Giai đoạn mù

5 người đánh giá song song chạy trước, được điều phối trong một tin nhắn duy
nhất. Không ai được đưa đầu ra của ai.

Đây là tính chất chịu lực của cả vòng đánh giá, và cũng là tính chất suy giảm
một cách lặng lẽ. Nhiễm chéo không sinh ra lỗi; nó sinh ra sự đồng thuận. Một
chuyên gia đã đọc phán quyết sàng lọc sẽ trôi dần về phía xác nhận nó, và năm
bản báo cáo đồng ý với nhau trông giống một đồng thuận mạnh chứ không giống một
ý kiến được nhắc lại năm lần. Đồng thuận xuyên suốt giai đoạn mù là tín hiệu
đáng tin nhất mà quy trình sinh ra, và nó chỉ đáng giá vì năm bên đó không nói
chuyện được với nhau.

Mỗi vai chỉ được đưa đúng những gì vai đó thực sự có:

| Vai | Được đưa | Bị giữ lại, và vì sao |
| --- | --- | --- |
| Người sàng lọc | Văn bản CV, chức danh, công ty, cấp bậc | Thư xin việc. Nó đang mô phỏng mười một giây, và một người sàng lọc đã đọc thư thì không còn là người sàng lọc. |
| Chuyên viên phân tích yêu cầu | CV, thư xin việc, toàn văn tin tuyển dụng, cấp bậc | Không giữ lại gì. Việc của nó là đối chiếu từng điều kiện với bằng chứng. |
| Trình mô phỏng ATS | Văn bản CV, toàn văn tin tuyển dụng, và tệp nguồn `.tex` hoặc `.docx` nếu có | Không giữ lại gì, nhưng lưu ý rằng nó được đưa *tệp nguồn* một cách có chủ ý: bảng, cột và vị trí đặt phần đầu trang là vô hình trong văn bản trích xuất, và đó đúng là thứ nó tồn tại để bắt. |
| Người đọc mệt mỏi | CV, thư xin việc | Mọi chỉ dẫn bảo nó phán xét xem văn bản có phải do AI viết không. Đó là một câu hỏi khác và không phải câu hỏi của vai này. |
| Chuyên viên phân tích nhóm ứng viên | Mọi thứ, cộng với lịch sử ứng tuyển trước đó và các tỷ lệ chuyển đổi đã quan sát được | Không giữ lại gì. Nó cần nhiều ngữ cảnh nhất trong năm bên. |

Bản CV mà mọi vai đọc là đầu ra của `pdftotext`, không phải tệp nguồn LaTeX hay
Markdown. Đánh giá tệp nguồn là đánh giá một tài liệu sẽ không ai nhìn thấy. Nếu
văn bản trích xuất ra rỗng hoặc lộn xộn, đó là một phát hiện chứ không phải một
sự cố công cụ: một hệ ATS nhìn thấy đúng những gì `pdftotext` nhìn thấy.

## Vì sao hai vai cuối chạy tuần tự

Quản lý tuyển dụng chạy sau khi cả năm bên trả về, và đọc cả năm. Người phản
biện chạy sau quản lý tuyển dụng, và thấy mọi thứ kể cả phần đó.

Xếp chúng theo thứ tự này tốn thời gian đồng hồ và mua về đúng thứ mà giai đoạn
mù không thể cho: một bên có thể cân năm báo cáo với nhau, rồi một bên nữa có
thể tấn công chính phép cân đó. Một người phản biện chạy song song với quản lý
tuyển dụng sẽ đang tranh cãi với một bản tổng hợp mà nó chưa từng đọc.

Người phản biện là **tự động, không phải có điều kiện**. Một bước phản nghiệm
chỉ chạy khi bộ điều phối cảm thấy không chắc chắn sẽ tự bỏ qua chính mình đúng
vào những ca mà sự chắc chắn là đặt nhầm chỗ.

## Tiên nghiệm được truyền nguyên văn, kể cả khi chúng rỗng

Cả chuyên viên phân tích nhóm ứng viên lẫn người phản biện đều nhận khối
`calibration_priors` từ `preferences.yaml` đúng như nó được viết.

Tóm nó lại thành “ứng viên này chuyển đổi kém” là bóc mất cỡ mẫu, mà cỡ mẫu là
thứ duy nhất nói cho biết con số đó đáng được cân bao nhiêu. Còn bỏ hẳn khối đó
khi nó chưa được đặt thì đọc lên với tác nhân giống một lần chạy bình thường chứ
không phải một lần chạy chưa hiệu chỉnh, mà một ước lượng chưa hiệu chỉnh nhưng
không được gắn nhãn như vậy thì tệ hơn là không có ước lượng nào, vì ở phía sau
nó không phân biệt được với một ước lượng đã hiệu chỉnh.

Ở đâu một tỷ lệ quan sát được có cỡ mẫu từ năm trở lên, chuyên viên phân tích
nhóm ứng viên được chỉ thị dùng nó thay cho tiên nghiệm của chính nó cho kênh
đó, và phải nói rằng nó đã làm vậy.

## Người gác cổng

Kỹ năng điều phối chính là người gác cổng. Nó không phải một trong các vai, và
điều đó là có chủ ý: các vai được chỉnh cho khắc nghiệt, một phần những gì chúng
đưa ra là sai, và không thứ gì được chỉnh cho khắc nghiệt lại có thể đồng thời
là thứ quyết định phải vứt bỏ cái gì.

Nó đối chiếu mỗi vai với bản điều lệ của chính vai đó: người sàng lọc có ở lại
trong mười một giây không, hay đã trích dẫn thứ gì đó ở trang thứ ba? Trình mô
phỏng ATS có gắn cờ một kiểu định dạng mà các bộ phân tích hiện đại xử lý tốt
không? Người đọc mệt mỏi có gắn cờ một dấu hiệu giọng văn cố ý, đã được ghi lại
trong chính tác nhân giọng văn của bạn, như thể đó là một lỗi không?

Hai loại lập luận của người phản biện bị **gạch bỏ** thay vì được cân:

1. **Điều khoản hợp đồng ở giai đoạn nhận offer.** Tiền chuyển chỗ ở, thưởng ký
   hợp đồng, cổ phần, ngày bắt đầu, việc mua lại một khoản hoàn trả. Những thứ
   này được thương lượng sau khi đã có offer. Loại một hồ sơ vì khoản tiền vẫn
   còn thương lượng được, ngay ở giai đoạn ứng viên có ít đòn bẩy nhất, là một
   lỗi phạm trù.
2. **Một vị trí lân cận chưa được đánh giá.** Một chỗ ngồi trông đẹp hơn ở nơi
   khác trong cùng công ty không phải là một đầu vào, trừ khi nó đã được đánh
   giá đầy đủ và bạn đã yêu cầu đem nó ra cân. Việc sắp thứ tự giữa các vị trí
   là quyết định của bạn.

Mọi thứ khác mà người phản biện nêu ra đều nằm trong phạm vi: xác suất chuyển
đổi, cấu trúc kênh, vị trí trong nhóm ứng viên, các khoảng hụt về điều kiện, các
tuyên bố quá đà, các phép thử hoán đổi bị trượt, mật độ tài liệu, tín hiệu về độ
khớp cấp bậc, và lịch sử ứng tuyển bất lợi tại công ty đích.

Cả những chân lập luận bị gạch lẫn những chân sống sót đều được ghi vào
`role_analysis.md`. Chỉ ghi mỗi kết quả sẽ khiến cổng chặn này không thể cải
thiện được, vì những báo động giả mà nó bắt được sẽ trở nên vô hình ngay khoảnh
khắc nó bắt được chúng.

## Trần ba vòng

Các vòng được đem ra so, chứ không chỉ chạy lại. Một vấn đề bị gắn cờ ở nhiều
hơn một vòng là thật; một vấn đề bị gắn cờ một lần là nhiễu. Tín hiệu đó chỉ tồn
tại nếu vòng đánh giá chạy nhiều hơn một lần, và đó là lý do builder mặc định
chạy nó hai lần.

Mỗi vòng dùng **các thực thể tác nhân mới**. Một vai đã nhìn thấy phán quyết của
chính mình thì không thể suy lại nó một cách độc lập, nên tái dùng một báo cáo
qua các vòng là biến ý kiến thứ hai thành một tiếng vọng.

Ba vòng là trần. Quá đó thì những khoảng hụt còn lại là chuyện cấu trúc, và đầu
ra trung thực là nói thẳng như vậy thay vì chạy vòng thứ tư và sinh thêm chỉnh
sửa.

## Trên một harness không điều phối được tác nhân con

Codex và Gemini CLI không có cơ chế điều phối tác nhân con. Vòng đánh giá vẫn
chạy: các vai được nhập lần lượt, trong cùng một ngữ cảnh, mỗi báo cáo được viết
ra xong trước khi vai kế tiếp bắt đầu.

Có hai thứ suy giảm, và đáng biết là thứ nào. Nó chậm hơn, điều này không quan
trọng lắm. Và giai đoạn mù không còn mù nữa, điều này thì quan trọng: đúng kiểu
nhiễm chéo mô tả ở trên là thứ mà một ngữ cảnh dùng chung mang trở lại. Kỹ năng
này chỉ thị cho mô hình viết trọn từng báo cáo trước khi bắt đầu báo cáo kế
tiếp, việc đó hạn chế được độ trôi mà không loại bỏ được nó.
