# Quy trình, từng giai đoạn một

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../../docs/architecture/pipeline.md">English</a> ·
  <a href="../../../zh-CN/docs/architecture/pipeline.md">简体中文</a> ·
  <a href="../../../es/docs/architecture/pipeline.md">Español</a> ·
  <a href="../../../pt-BR/docs/architecture/pipeline.md">Português (BR)</a> ·
  <strong>Tiếng Việt</strong> ·
  <a href="../../../en-x-aibro/docs/architecture/pipeline.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

## Toàn bộ vòng lặp

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../../../docs/diagrams/pipeline-overview-dark.svg">
  <img alt="Slushpile từ đầu đến cuối. Hàng một, từ trái sang phải: onboard, phỏng vấn và nạp vào một CV để viết ra profile, preferences và stories; job board search, trích xuất tin tuyển dụng nguyên văn rồi chấm điểm độ phù hợp neo theo nhóm ứng viên và giá trị kỳ vọng theo kênh; application builder, tạo ra góc tiếp cận, CV, thư, lượt viết theo giọng văn và bước khử dấu vết AI; và adversarial review, 7 người đánh giá, trong đó 5 người đánh giá song song không thấy được nhau, trả về một phán quyết cho mỗi kênh. Builder và review được nối bằng một mũi tên hai chiều ghi nhãn tối đa ba vòng. Luồng đi từ review xuống một hộp màu xanh, bạn tự gửi nó đi, có ghi chú rằng không kỹ năng nào chạm vào cổng nộp hồ sơ, email hay biểu mẫu. Hàng hai đọc ngược từ phải sang trái: kết quả được ghi lại, rồi status, so sánh những dự đoán của quy trình với kết quả thực tế, rồi một mũi tên nét đứt ghi nhãn tiên nghiệm đi vào hộp không gian làm việc chứa profile.md, preferences.yaml, stories.md và job_search.md. Một mũi tên nét đứt nối không gian làm việc quay lại onboard, ghi nhãn do onboarding ghi ra, được mọi giai đoạn đọc." src="../../../../docs/diagrams/pipeline-overview-light.svg">
</picture>

Xương sống gồm ba lệnh: `onboard` chạy một lần cho mỗi không gian làm việc, rồi
`job-board-search` và `application-builder` chạy cho từng công ty và từng vị
trí. Chính builder tự điều phối `explore-experience`, `adversarial-review` và
`removing-ai-tells`.

Vòng lặp ở dưới cùng là phần không có thứ tương đương trong một công cụ tối ưu
CV. Kết quả được ghi lại, `status` hồi quy những gì quy trình đã dự đoán với
những gì thực sự xảy ra, và các tiên nghiệm đã hiệu chỉnh quay về
`preferences.yaml`, nơi lần tìm kiếm tiếp theo đọc chúng. Xem
[memory-and-calibration.md](memory-and-calibration.md).

## Chú giải

Mọi sơ đồ trên trang này đều rút từ một bộ từ vựng lớp duy nhất, được định nghĩa
trong `docs/diagrams/theme-light.d2` và `theme-dark.d2`. Hai tệp chủ đề đó và
bảng này được `tests/test_docs.py` đối chiếu với nhau.

| Lớp | Nghĩa |
| --- | --- |
| `stage` | Một bước thông thường mà chính kỹ năng điều phối tự thực hiện |
| `agent` | Một vai được điều phối: một tác nhân con có định nghĩa riêng trong `agents/` |
| `gate` | Một cổng chặn hoặc một vòng lặp có trần: chỗ mà lần chạy có thể lặp lại, kẹt lại, hoặc dừng hẳn |
| `memory` | Một tệp bền vững trong không gian làm việc, ghi một lần và được mọi giai đoạn sau đó đọc |
| `human` | Chỗ duy nhất bắt buộc phải có bạn |
| `terminal` | Một trạng thái kết thúc của sơ đồ đó |
| `phase` | Một vùng chứa gom những ô chạy cùng nhau |
| `flow` | Một cạnh xuôi thông thường |
| `loop` | Một cạnh ngược: làm lại, đánh giá lại, thêm một vòng nữa |
| `writeback` | Một cạnh ghi vào trí nhớ của không gian làm việc |

Phân biệt giữa `stage` và `agent` là chỗ đáng đọc kỹ nhất. Một hộp `agent` là
một tác nhân con có định nghĩa riêng và ngữ cảnh riêng. Trên một harness không
điều phối được tác nhân con, chính những hộp đó là thứ sụp lại thành một ngữ
cảnh duy nhất, và cú sụp đó là toàn bộ khác biệt giữa một lần chạy đầy đủ và
một lần chạy đã suy giảm.

## `/slushpile:onboard`

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../../../docs/diagrams/phase-onboard-dark.svg">
  <img alt="Các giai đoạn của onboarding. Hàng một: nạp vào một CV ở bất kỳ định dạng nào hoặc một bản xuất từ LinkedIn; phỏng vấn để lấp những khoảng trống mà một tài liệu không lấp được, với các con số đều được cho kèm mốc tham chiếu; profile.md, được mô tả là kho chất liệu mà một CV được cắt ra từ đó chứ không phải bản thân một CV; preferences.yaml, chứa phương pháp tính lương và các ràng buộc, với calibration_priors để trống. Hàng hai đọc ngược từ phải sang trái: stories.md, bốn đến tám câu chuyện kể được, kèm các con số; một cổng chặn về tác nhân giọng văn, chỉ bạn tới tác nhân của chính bạn và giữ is_mine ở false cho tới khi bạn có một cái; scaffold, ghi ra job_search.md cùng companies.md rồi chạy kiểm tra bộ công cụ; và xác minh rồi bàn giao, nơi mọi lượt kiểm tra đều được báo cáo, kể cả những lượt đã qua." src="../../../../docs/diagrams/phase-onboard-light.svg">
</picture>

Onboarding là một cuộc phỏng vấn, không phải một biểu mẫu. Nó chạy một lần và
mọi thứ sau đó đều đọc những gì nó đã ghi.

Hai trong số các bước của nó là cổng chặn chứ không phải công việc. Bước tác
nhân giọng văn từ chối tự dựng lấy một hồ sơ giọng văn: một hồ sơ chắp vá từ vài
mẫu viết đọc lên chỉ là giọng mặc định của mô hình khoác tên bạn, và bạn sẽ tin
nó vì trông nó có vẻ đã hoàn chỉnh. Bước đó đặt `voice.is_mine: false` và thay
vào đó chỉ bạn tới
[written-voice-replication](https://github.com/aaddrick/written-voice-replication).
Bước xác minh nêu rõ những lượt kiểm tra nào đã *qua*, chứ không chỉ những lượt
đã trượt, vì một lượt kiểm tra chỉ báo cáo thất bại thì không thể phân biệt với
một lượt chưa từng chạy.

`calibration_priors` được để trống một cách có chủ ý. Một tiên nghiệm bịa ra là
một ràng buộc bạn chưa bao giờ chọn, nó âm thầm loại đi các vị trí vì một lý do
bạn không nhìn thấy được. Về sau nó sẽ được điền từ kết quả thật, hoặc nó cứ
trống và mọi ước lượng ở phía sau đều bị gắn nhãn là chưa hiệu chỉnh.

## `/slushpile:job-board-search`

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../../../docs/diagrams/phase-search-dark.svg">
  <img alt="Các giai đoạn của job board search. Hàng một: khám phá, tìm ra URL trang tuyển dụng và chạy vài truy vấn trước khi phân loại nhanh theo chức danh; thu nguyên văn, lấy tin tuyển dụng đúng như nó được viết chứ không phải bản tóm tắt; ước lượng nhóm ứng viên, mô tả những ai khác cũng nộp dưới dạng các nguyên mẫu p50, p75 và p90; và điểm phù hợp, nơi con số được lấy là phân vị trong nhóm ứng viên chứ không phải mức khớp từ khóa. Hàng hai đọc ngược từ phải sang trái: ma trận giá trị kỳ vọng theo kênh, trải trên nộp nguội, giới thiệu nội bộ, chủ động liên hệ và thu hút tự nhiên, nơi hạng được lấy theo kênh tốt nhất thực sự có sẵn; tiêu chí loại về lương, địa điểm và quyền truy cập thông tin mật, được kiểm tra và nêu rõ dù kết quả ra sao; một cổng phản biện chạy trước khi các hạng được chốt và có thể hạ hạng hoặc loại thẳng một vị trí; và các thư mục vị trí, mỗi vị trí một thư mục kèm mô tả công việc và phần phân tích, cùng với tệp theo dõi và tệp công ty được cập nhật." src="../../../../docs/diagrams/phase-search-light.svg">
</picture>

Đây là giai đoạn có lợi suất cao nhất, và là giai đoạn mà phần lớn công cụ khác
không có. Mọi thứ ở phía sau tốn của bạn một buổi chiều cho mỗi hồ sơ. Giai đoạn
này tốn vài phút và có thể kết thúc bằng “đừng nộp cái nào trong số này cả”.

Tin tuyển dụng được thu lại **nguyên văn**. Về sau có 3 tác nhân phân tích trực
tiếp đoạn văn bản đó, là chuyên viên phân tích yêu cầu, trình mô phỏng ATS và
chuyên viên phân tích nhóm ứng viên, và một tin tuyển dụng đã bị tóm tắt sẽ âm
thầm xóa mất đúng cái cách diễn đạt điều kiện mà cả ba tồn tại để đối chiếu.

Cổng phản biện chạy *trước* khi các hạng được chốt chứ không phải sau, vì một
danh sách hạng mà bạn đã đọc rồi là một danh sách hạng mà bạn đã trót cam kết
theo. Xem [scoring.md](scoring.md) để biết các hạng nghĩa là gì và tiêu chí loại
kiểm tra những gì.

## `/slushpile:application-builder`

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../../../docs/diagrams/phase-build-dark.svg">
  <img alt="Các giai đoạn của application builder. Hàng một: góc tiếp cận, chọn CV nền, luận điểm, câu mở đầu và một câu chuyện duy nhất đáng kể; CV, được điều chỉnh rồi biên dịch, đọc phần văn bản trích xuất chứ không phải tệp nguồn; thư xin việc, do tác nhân giọng văn được nêu tên trong preferences.yaml viết; và khử dấu vết AI, chạy removing-ai-tells với bộ điều phối kiểm duyệt từng thay đổi một. Hàng hai đọc ngược từ phải sang trái: adversarial review vòng một, cho ra điểm ATS, các phép thử hoán đổi và giá trị kỳ vọng theo từng kênh; sửa, các chỉnh sửa cơ học trước rồi mới tới chiều sâu lấy từ profile.md; adversarial review vòng hai, có cổng quyết định đọc phán quyết của kênh có giá trị kỳ vọng cao nhất, nối về bước sửa bằng một vòng lặp nét đứt ghi nhãn tối đa ba vòng; và kết thúc, lần dựng cuối cùng với application.yaml, hồ sơ và tệp theo dõi được cập nhật." src="../../../../docs/diagrams/phase-build-light.svg">
</picture>

Builder viết, rồi tấn công chính thứ nó vừa viết. Một mô hình bị hỏi bản nháp
của chính nó có tốt không sẽ trả lời là có, rất dài dòng, nên builder không bao
giờ hỏi: nó giao tài liệu cho một vòng đánh giá không có lợi ích gì trong đó.

Thứ tự các bản sửa có ý nghĩa. Sửa cơ học đi trước vì chúng rẻ và không mơ hồ:
từ khóa còn thiếu, mốc thời gian chỉ ghi năm, một gạch đầu dòng bê gần như
nguyên văn từ tin tuyển dụng. Chỉ sau đó nó mới thử tới loại đắt đỏ, tức là khi
một mục quá mỏng phải được đắp thêm từ `profile.md`; và ở đó, nếu chất liệu thực
sự không có trong hồ sơ, nó chạy `/slushpile:explore-experience` thay vì bịa ra.

**Ba vòng là trần.** Nếu đến vòng thứ ba mà phán quyết vẫn không nhúc nhích thì
khoảng cách là chuyện cấu trúc, và sửa thêm là cử động chứ không phải tiến bộ.
Cái trần này tồn tại vì lựa chọn còn lại là một vòng lặp luôn tìm ra được cái gì
đó, mà một vòng đánh giá luôn tìm ra được cái gì đó thì không thể phân biệt với
một vòng đánh giá chẳng tìm ra gì.

## `/slushpile:adversarial-review`

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../../../docs/diagrams/phase-review-dark.svg">
  <img alt="Vòng đánh giá đối kháng. Trước hết là gom tài liệu: chạy pdftotext trên tệp PDF đã biên dịch, cộng thêm mô tả công việc, phần phân tích vị trí, preferences.yaml và job_search.md. Những thứ đó nạp vào một vùng chứa gồm 5 người đánh giá song song được điều phối trong cùng một tin nhắn, không ai thấy báo cáo của ai: người sàng lọc trong mười một giây và chỉ với bản CV, chuyên viên phân tích yêu cầu trong ba mươi giây đối chiếu từng điều kiện một, trình mô phỏng ATS đóng vai một bộ phân tích cú pháp chứ không phải một người đọc, người đọc mệt mỏi đang ở hồ sơ thứ sáu mươi mốt trong tám mươi, và chuyên viên phân tích nhóm ứng viên hỏi xem còn ai khác đang xếp hàng. Một cạnh ghi nhãn cả năm đều trả về dẫn tới quản lý tuyển dụng, bên này đọc cả năm bản báo cáo và cho ra một phán quyết cho mỗi kênh, với chất lượng được chấm tách rời khỏi giá trị kỳ vọng. Tiếp đó là người phản biện, thấy được mọi thứ kể cả phần của quản lý tuyển dụng và có thể lật ngược nó, và không bao giờ là tùy chọn. Tiếp đó là người gác cổng, chính là bộ điều phối chứ không phải một tác nhân, nó gạch bỏ các báo động giả và các phán quyết loại nằm ngoài phạm vi, suy lại kết luận ròng, và chạy lại toàn bộ quy trình bằng những thực thể mới khi tài liệu thay đổi. Cuối cùng là trình bày và ghi nhận, xếp ưu tiên theo mức tác động lên kênh có giá trị kỳ vọng cao nhất chứ không theo tác nhân nào la to nhất." src="../../../../docs/diagrams/phase-review-light.svg">
</picture>

5 người đánh giá song song trong vùng chứa được điều phối trong một tin nhắn duy
nhất và không thấy được phát hiện của nhau. Mỗi bên chỉ được đưa đúng những gì
vai của nó thực sự có: người sàng lọc không bao giờ được cho xem thư xin việc,
vì một người sàng lọc đã đọc thư thì không còn là người sàng lọc nữa.

Người gác cổng là kỹ năng điều phối, không phải một tác nhân. Các vai được đặt
ra để khắc nghiệt một cách có chủ ý và một phần những gì chúng đưa ra là sai,
nên phải có cái gì đó đứng ra phán đoán trên đầu ra của chúng, và cái đó không
thể là một trong số chúng.

[the-review.md](the-review.md) nói về thứ tự điều phối, mỗi vai bị giữ lại không
cho xem thứ gì, và người gác cổng được phép gạch bỏ những phát hiện nào.
