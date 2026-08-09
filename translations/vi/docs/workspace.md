# Không gian làm việc

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../docs/workspace.md">English</a> ·
  <a href="../../zh-CN/docs/workspace.md">简体中文</a> ·
  <a href="../../es/docs/workspace.md">Español</a> ·
  <a href="../../pt-BR/docs/workspace.md">Português (BR)</a> ·
  <strong>Tiếng Việt</strong> ·
  <a href="../../en-x-aibro/docs/workspace.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

`/slushpile:onboard` chạy trong thư mục **của bạn**, không phải trong bản
checkout của plugin, và mọi thứ quy trình biết về bạn đều nằm ở đó.

Thư mục đó sẽ chứa toàn bộ lịch sử công việc của bạn, các con số lương thưởng của
bạn, và các ràng buộc của bạn. Hãy giữ nó trong một kho **riêng tư**, hoặc không
trong kho nào cả. Onboarding sẽ nói với bạn điều này, và nó sẽ không tự khởi tạo
kho giúp bạn, cũng không thêm remote: đó là quyết định cần đưa ra một cách có chủ
đích chứ không phải thứ thừa hưởng từ một bước cài đặt.

## Onboarding ghi ra những gì

```
profile.md          every factual claim about you
preferences.yaml    compensation, location, constraints, calibration priors
stories.md          four to eight tellable stories, with the numbers attached
job_search.md       the tracker: applications, outcomes, calibration
companies.md        one line per company ever looked at
applications/       one folder per role, created by job-board-search
```

### `profile.md`

**Không phải một CV.** Đây là cái kho mà một CV được cắt ra từ đó, dài gấp nhiều
lần bất cứ thứ gì bạn từng gửi đi, bởi CV là một lựa chọn còn đây là thứ được lựa
ra từ đó.

Mọi con số trong đó đều mang theo một mốc đối chiếu, hoặc được đánh dấu rõ ràng
là không cần mốc. "Giảm độ trễ 40%" là vô dụng cho tới khi người đọc biết 40% của
cái gì, và một con số không nguồn chính là con số bạn sẽ bị hỏi trong buổi phỏng
vấn và không trả lời được. Những con số chưa xác minh được nguồn thì bị đánh dấu
`UNVERIFIED` chứ không bị bỏ đi.

Nó lớn dần. Khi một vòng đánh giá nói rằng một mục còn mỏng,
`/slushpile:explore-experience` phỏng vấn bạn và ghi những gì nó tìm được trở lại
vào đây, để bộ hồ sơ kế tiếp khởi đầu từ đó.

### `preferences.yaml`

Nửa dành cho máy đọc. Phương pháp và mốc lương thưởng, ràng buộc về địa điểm và
chuyển vùng, tình trạng chứng nhận an ninh và bằng cấp, những điểm khác biệt bạn
tự nhận, tác nhân giọng văn của bạn, và `calibration_priors`.

Hai trường làm nhiều việc hơn phần còn lại:

```yaml
voice:
  agent: "your-name-voice"
  is_mine: true
```

Chừng nào `is_mine` còn là false, mọi kỹ năng có soạn văn bản đều cảnh báo bạn
trước khi chạy. Xem [Tác nhân giọng văn của bạn](voice.md).

`calibration_priors` khởi đầu rỗng và ở yên như vậy cho tới khi bạn có từ năm bộ
hồ sơ đã ngã ngũ trở lên trên một kênh. Một tiên nghiệm rỗng nghĩa là các tác
nhân dùng giá trị mặc định đi kèm và ghi nhãn ước lượng của chúng là chưa hiệu
chỉnh, và đó là hành vi đúng: một tiên nghiệm tính từ hai kết quả đẩy việc chấm
điểm ra xa thực tế hơn là không có tiên nghiệm nào, lại còn xuất hiện với vẻ
ngoài thực nghiệm.

### `stories.md`

Bốn đến tám câu chuyện bạn thực sự kể được, kèm theo các con số. Trình dựng hồ
sơ chọn một câu cho mỗi bộ hồ sơ; buổi phỏng vấn mà rốt cuộc bạn có được sẽ chạy
trên chính những câu chuyện này.

### `job_search.md`

Tệp theo dõi, và cũng là trí nhớ dài hạn của quy trình. Các bộ hồ sơ, kết quả
của chúng, những lần nộp trước ở từng công ty, và một mục `Calibration` mà
`/slushpile:status` viết lại từ chính kết quả của bạn.

Lịch sử nộp hồ sơ trước đó ở một công ty được chuyên viên phân tích nhóm ứng
viên và người phản biện đọc trong lúc đánh giá. Một lần bị từ chối trước đó ở
cấp **cao hơn** có ảnh hưởng thực sự: nhà tuyển dụng nhìn thấy toàn bộ lịch sử
trong hệ thống theo dõi ứng viên, và một lần nộp sau đó ở cấp thấp hơn bị đọc
thành một cú tụt nhiều cấp.

### `companies.md`

Một dòng cho mỗi công ty bạn từng ngó qua, để lần tìm kiếm thứ hai ở cùng công ty
đó khởi đầu từ những gì lần đầu đã tìm ra.

## Thư mục vai trò

`/slushpile:job-board-search` tạo một thư mục cho mỗi vai trò sống sót qua bước
phân hạng:

```
applications/<Company>/<Function>/<Role>/
  job_description.md    the posting, captured verbatim
  role_analysis.md      pool position, channel EV, kill criteria, contrarian notes
  application.yaml      the record: verdicts, scores, channel used, outcome
  resume.tex            copied per role by the builder
  cover_letter.tex      copied per role by the builder
```

Tin tuyển dụng được lưu **nguyên văn**, không tóm tắt. 3 tác nhân phân tích trực
tiếp đoạn văn bản đó trong lúc đánh giá, và một bản diễn giải lại sẽ âm thầm xóa
mất đúng cái câu chữ về yêu cầu mà chúng sinh ra để kiểm tra.

`application.yaml` là tệp mà `/slushpile:status` đọc để dựng hàng đợi và để hồi
quy dự đoán trên kết quả thực. Nó cũng là tệp cần cập nhật khi có chuyện xảy ra:
một lần bị từ chối, một vòng sàng lọc, một buổi phỏng vấn, một lời mời làm việc.
Không thứ gì khác trong quy trình học được điều đó, bởi quy trình không bao giờ
nộp gì và không bao giờ nhìn thấy hồi âm.

Các mẫu tài liệu được sao chép **vào từng thư mục vai trò** thay vì giữ ở gốc
không gian làm việc. Một bản nguyên vẹn ở gốc trở thành một bản lỗi thời ngay
khoảnh khắc bộ hồ sơ đầu tiên đi chệch khỏi nó.

## Những gì plugin không bao giờ giữ

Không gì trong `skills/` hay `agents/` mã hóa cứng một dữ kiện về bạn. Không mức
lương sàn, không địa điểm, không tình trạng chứng nhận an ninh, không tên nhà
tuyển dụng. Một kỹ năng cần một trong những thứ đó sẽ đọc nó từ
`preferences.yaml` lúc chạy, và một cổng kiểm tra CI sẽ đánh trượt bản dựng nếu
một dữ kiện cá nhân rò rỉ vào plugin.

Đó chính là thứ khiến không gian làm việc mang đi được và plugin cập nhật được:
bạn có thể cài lại, fork, hoặc cập nhật slushpile mà không đụng tới bất cứ thứ gì
thuộc về chính bạn. Xem [Dữ liệu cá nhân](architecture/personal-data.md).
