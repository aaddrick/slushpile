# Dữ liệu cá nhân

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../../docs/architecture/personal-data.md">English</a> ·
  <a href="../../../zh-CN/docs/architecture/personal-data.md">简体中文</a> ·
  <a href="../../../es/docs/architecture/personal-data.md">Español</a> ·
  <a href="../../../pt-BR/docs/architecture/personal-data.md">Português (BR)</a> ·
  <strong>Tiếng Việt</strong>
</p>

<!-- END GENERATED language-nav -->

## Ranh giới

Plugin là mã nguồn công khai. Không gian làm việc là lịch sử nghề nghiệp, các
con số về lương và các ràng buộc của một con người cụ thể. Chúng là hai thứ khác
nhau và nằm ở hai thư mục khác nhau, và gần như mọi quy tắc trên trang này đều
suy ra từ đúng một câu đó.

`/slushpile:onboard` được chạy trong thư mục của chính bạn, không phải trong bản
checkout của plugin. Nó ghi `profile.md`, `preferences.yaml` và `stories.md` vào
đó. Onboarding nói thẳng rằng thư mục đó nên là một kho mã **riêng tư** hoặc
không phải kho mã nào cả, và nó sẽ không khởi tạo kho mã hay thêm remote: đó là
một quyết định phải đưa ra một cách có chủ ý, không phải hệ quả phụ của việc
dựng một không gian làm việc.

## Không thứ gì trong `skills/` hay `agents/` được phép ghi cứng một dữ kiện về bất kỳ người dùng nào

Không có sàn lương. Không có bảng giá thuê nhà theo thành phố. Không có quốc
tịch, không có tình trạng quyền truy cập thông tin mật, không có tên nhà tuyển
dụng nào được nêu như của chính người dùng, không có câu chuyện nào được kể đích
danh, không có câu “ứng viên sẵn sàng chuyển chỗ ở”. Một kỹ năng cần một trong
những thứ đó thì đọc nó từ `preferences.yaml` lúc chạy.

Kiểu hỏng mà điều này ngăn chặn là cụ thể và lặng lẽ. Một sàn lương ghi cứng
không báo lỗi; nó loại đi các vị trí, trông có vẻ đúng đắn, vì một lý do người
dùng chưa bao giờ chọn và không nhìn thấy được. Một câu “sẵn sàng chuyển chỗ ở”
ghi cứng cũng không báo lỗi; nó sinh ra mười hai hồ sơ khẳng định về một người
một điều có thể không đúng.

Các ví dụ minh họa có nêu tên công ty thật thì không sao, và còn hữu ích, vì
chúng dạy được khuôn mẫu. *“Phần lớn ứng viên cho mảng hoạch định năng lực đều
đến từ một phía”*, làm ví dụ cho một luận điểm phụ thuộc vào từng công ty, là
dạy. *“Ứng viên có mười năm trong lĩnh vực hệ thống điều khiển công nghiệp”* là
một chỗ rò rỉ.

Lưu ý rằng ví dụ thứ hai đã phải được diễn đạt lại thì mới xuất hiện được trên
trang này. Ví dụ thật nêu tên một lĩnh vực mà `check_no_pii.py` khớp trúng, và
chính tệp này là một trong những tệp nó quét, tức là cổng chặn đang hoạt động
đúng như thiết kế, ngay trên trang tài liệu mô tả nó.

## Cổng chặn

```bash
python3 scripts/check_no_pii.py
```

Nó quét `skills/`, `agents/`, `templates/` và `docs/` để tìm những khuôn mẫu đã
rò rỉ lần trước, mỗi khuôn mẫu kèm lý do vì sao nó bị tính là rò rỉ: danh tính
tác giả, một nhà tuyển dụng trước đây được nêu như của chính người dùng, một nơi
ở ghi cứng, một mốc lương ghi cứng, một tình trạng quốc tịch hoặc quyền truy cập
thông tin mật được nêu như sự thật, một chứng chỉ được nêu như sự thật, thông
tin liên hệ thật, và những tham chiếu tới các tệp chỉ tồn tại trong kho mã riêng
tư mà plugin này được sản phẩm hóa ra từ đó.

Các khuôn mẫu được đặt hẹp một cách có chủ ý. Một khuôn mẫu rộng cứ nổ vào văn
xuôi hợp lệ sẽ bị tắt đi trong vòng một tuần, và một lượt kiểm tra đã bị tắt thì
còn tệ hơn không có lượt kiểm tra nào, vì nó đọc lên như thể đã được che phủ.

Một khuôn mẫu rò rỉ mới lọt qua được thì thuộc về cái script đó, không thuộc về
một bình luận review.

## Ngoại lệ duy nhất, và giới hạn của nó

Các tác nhân giọng văn được miễn trừ khỏi các khuôn mẫu về **danh tính**, và chỉ
những khuôn mẫu đó. Một tác nhân giọng văn *chính là* danh tính của một con người
theo đúng cách nó được dựng nên: nó được sinh ra từ một khối văn bản người đó
viết, được đặt tên theo họ, và các ví dụ few-shot của nó là những câu thật của
họ. Bóc danh tính ra khỏi nó là phá hủy chính sản phẩm ấy.

Thông tin liên hệ thì bị cấm ở mọi nơi, kể cả trong tác nhân giọng văn. Một số
điện thoại trong một tác nhân được phát hành là rò rỉ theo bất cứ cách hiểu nào.

Danh sách miễn trừ được lập theo từng tệp và từng khuôn mẫu, trong
`check_no_pii.VOICE_AGENTS`. Có một danh sách thứ hai, `ALLOWED`, dành cho mọi
thứ khác, và nó rỗng một cách có chủ ý. Mỗi mục trong đó sẽ là một cái lỗ, và
một cái lỗ trên cổng chặn này là vô hình cho tới khi hồ sơ của người khác nói
rằng họ sẵn sàng chuyển tới sống ở một thành phố họ chưa từng nhìn thấy.

## Quy trình không bao giờ nộp bất cứ thứ gì

Không kỹ năng nào chạm vào một cổng nộp hồ sơ, một email, hay một biểu mẫu. Mọi
giai đoạn đều ghi ra tệp. Bạn đọc chúng và bạn gửi chúng đi.

Đây là một tính chất về quyền riêng tư trước khi là một tính chất về an toàn:
một quy trình có nộp hồ sơ là một quy trình phải giữ thông tin đăng nhập, và
trong thiết kế này không có chỗ nào để đặt chúng mà lại không phải là máy của
chính bạn đang làm một việc bạn không tận mắt nhìn.
