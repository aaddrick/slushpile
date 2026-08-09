# Tác nhân giọng văn của bạn

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../docs/voice.md">English</a> ·
  <a href="../../zh-CN/docs/voice.md">简体中文</a> ·
  <a href="../../es/docs/voice.md">Español</a> ·
  <a href="../../pt-BR/docs/voice.md">Português (BR)</a> ·
  <strong>Tiếng Việt</strong>
</p>

<!-- END GENERATED language-nav -->

Một tác nhân thứ tám viết thư xin việc, và nó viết theo phong cách của đúng một
người cụ thể, dựng lên từ một kho văn bản do chính người đó viết.

Đó là phần duy nhất của quy trình này mà bạn phải tự mang tới.

## Tại sao lại là một tác nhân riêng

Thư xin việc là tài liệu duy nhất trong một bộ hồ sơ được kỳ vọng phải nghe như
tiếng của một con người. Một mô hình viết "bằng giọng của bạn" từ một CV sẽ cho
ra đúng giọng mặc định của mô hình với các dữ kiện của bạn nhét vào trong: thành
thạo, đồng đều, và bị nhận ra ngay là như vậy bởi người đọc thứ sáu mươi mốt
trong ngày.

Vì thế giọng văn không phải là một câu chỉ dẫn trong prompt. Nó là một định nghĩa
tác nhân được sinh ra từ vài nghìn từ văn bản thật của bạn, đo trên một tập các
chiều phong cách, kèm những mục tiêu bằng số mà một lượt sau có thể đối chiếu.

## Tự sinh giọng văn của bạn

[written-voice-replication](https://github.com/aaddrick/written-voice-replication)
là một quy trình riêng mà bạn chạy một lần. Nó phân tích một kho văn bản của bạn
trên 25 chiều và xuất ra một tác nhân giọng văn, một kỹ năng giọng văn, và một hồ
sơ bằng số với các mục tiêu đo được.

Gom kho văn bản mới là phần chậm, nên hãy bắt đầu trước khi bạn cần đến nó.

**Nguồn tốt:** bài đăng trên diễn đàn và Reddit, bài blog, tin nhắn Slack dài,
email gửi đồng nghiệp, mô tả pull request, tài liệu bạn viết một mình. Bản xuất
dữ liệu Reddit hoặc Twitter dùng được ngay.

**Nguồn tệ:** bất cứ thứ gì viết chung, bất cứ thứ gì người khác biên tập, bất cứ
thứ gì đã chạy qua một LLM, bất cứ thứ gì mang giọng của một tổ chức. Văn quảng
cáo và bản đánh giá hiệu suất là hai thứ tệ nhất: cả hai đều được viết bằng một
giọng không ai dùng một cách tự nguyện.

Vài nghìn từ là mức sàn. Dưới mức đó, kết quả đọc lên nhàn nhạt chung chung, và
đó là kiểu hỏng khó nhận ra nhất vì nó trông đã hoàn chỉnh.

## Trỏ slushpile vào nó

```yaml
voice:
  agent: "your-name-voice"
  is_mine: true
```

`voice.agent` gọi tác nhân bằng tên và không chỗ nào mã hóa cứng nó, và đó là
điều cho phép bạn thay bằng tác nhân của riêng mình mà không phải sửa plugin.

## Cho tới lúc đó

`aaddrick-voice` đi kèm như một ví dụ chạy được, để quy trình hoạt động ngay khi
vừa cài. Đó là giọng của tác giả plugin, không phải giọng của bạn. Thư viết bằng
nó sẽ nghe như một người lạ cụ thể nào đó: ổn để xem quy trình chạy, sai cho bất
cứ thứ gì bạn thực sự gửi đi.

Chừng nào `is_mine` còn là false, mọi kỹ năng có soạn văn bản đều cảnh báo bạn
trước khi chạy. Cảnh báo đó là thứ duy nhất đứng giữa bạn và mười hai bộ hồ sơ
gửi đi bằng giọng của một người lạ, nên đừng dập nó bằng cách đặt cờ thành true
trước khi tác nhân thực sự là của bạn.

## Giọng văn được dùng, và được bảo vệ, ra sao

`/slushpile:removing-ai-tells` cho lá thư chạy qua những phiên bản mới tinh của
tác nhân giọng văn, với kỹ năng điều phối đóng vai người gác cổng cho từng thay
đổi một. Một lượt chấp nhận mọi đề xuất sẽ mài lá thư trở lại về mức trung bình,
mà đó đúng là thứ tác nhân giọng văn sinh ra để ngăn.

Người đọc mệt mỏi trong vòng đánh giá cũng được đối chiếu với tác nhân giọng văn
của bạn vì cùng lý do đó. Một thói quen đặc trưng đã được ghi lại ở đó không trở
thành khiếm khuyết chỉ vì một người đánh giá gắn cờ nó, và gỡ nó đi chính là cách
một lá thư trôi ngược về chỗ nhàn nhạt.

Lưu ý rằng một tác nhân giọng văn, theo đúng cách nó được dựng, chính là danh
tính của một con người: sinh ra từ văn bản của người đó, đặt tên theo người đó,
và các ví dụ trong nó là những câu thật của người đó. Đó là lý do nó là tác nhân
duy nhất trong kho mã này được miễn khỏi các quy tắc dữ liệu cá nhân ràng buộc
mọi thứ còn lại, và là lý do phần miễn trừ dừng lại ở thông tin liên hệ. Xem
[Tác nhân và mô hình](architecture/agents-and-models.md).
