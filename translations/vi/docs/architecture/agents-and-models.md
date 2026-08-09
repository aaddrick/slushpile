# Tác nhân và mô hình

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../../docs/architecture/agents-and-models.md">English</a> ·
  <a href="../../../zh-CN/docs/architecture/agents-and-models.md">简体中文</a> ·
  <a href="../../../es/docs/architecture/agents-and-models.md">Español</a> ·
  <a href="../../../pt-BR/docs/architecture/agents-and-models.md">Português (BR)</a> ·
  <strong>Tiếng Việt</strong> ·
  <a href="../../../en-x-aibro/docs/architecture/agents-and-models.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

## Kỹ năng thì điều phối. Tác nhân thì làm đúng một việc.

Hai thứ đó là hai loại tệp khác nhau và ranh giới giữa chúng là ranh giới chịu
lực.

Một kỹ năng biết về quy trình: nó đang ở giai đoạn nào, cái gì đã chạy trước nó,
nó bàn giao cho ai. Một tác nhân chỉ biết việc của chính nó. **Một tác nhân biết
mình đang ở giai đoạn nào sẽ tối ưu cho giai đoạn đó thay vì làm việc của mình**:
một người sàng lọc được cho biết nó là người đầu tiên trong năm sẽ bắt đầu nói
nước đôi, vì nó đoán được rằng sẽ có người khác kiểm tra lại việc của nó.

Hệ quả kéo theo là quy tắc giữ cho đầu ra của vòng đánh giá so sánh được với
nhau:

**Các ràng buộc mang tính bắt buộc nằm trong định nghĩa tác nhân, không nằm
trong lời nhắc lúc điều phối.** Một bộ điều phối tự ứng biến thêm ràng buộc ở
mỗi lần chạy sẽ sinh ra những phát hiện không đem so được giữa các hồ sơ, và
điều đó phá hủy chính dữ liệu hiệu chỉnh mà cả hệ thống dựa vào. Giới hạn phạm
vi của người phản biện nằm trong `agents/slushpile-contrarian.md` vì lý do này,
và kỹ năng đánh giá được dặn rõ là không được nhắc lại hay nới rộng chúng.

Dữ liệu là ngoại lệ, và cần nói cho chính xác chỗ phân biệt.
`calibration_priors` đi vào lời nhắc lúc điều phối vì nó thay đổi *những gì tác
nhân biết*. Giới hạn phạm vi ở lại trong định nghĩa vì chúng thay đổi *những gì
tác nhân được phép nói*. Thứ nhất thay đổi theo từng lần chạy là chủ ý; thứ hai
thì không được phép.

## Mỗi tác nhân đều khai báo một mô hình

<!-- BEGIN GENERATED agent-table: scripts/sync_docs.py -->

| # | Agent | Model | Simulates |
|---|---|---|---|
| 1 | `slushpile-triage-screener` | sonnet | 11 seconds, F-pattern, 347 resumes already read today |
| 2 | `slushpile-requirements-analyst` | sonnet | 30 seconds, methodical, checks every qualification against evidence |
| 3 | `slushpile-ats-simulator` | sonnet | A parser. Not a reader. Structure, keywords, and years-of-experience math |
| 4 | `slushpile-fatigued-reader` | sonnet | Application #61 of 80. What annoys, what gets skimmed, what closes the tab |
| 5 | `slushpile-pool-analyst` | opus | A recruiter who knows what the queue actually looks like |
| 6 | `slushpile-hiring-manager` | opus | The person who has to justify the interview slot to their skip-level |
| 7 | `slushpile-contrarian` | opus | Whoever should have asked whether any of this was worth doing |

Plus the voice agent, `aaddrick-voice`, which the review never dispatches and
which is named in `preferences.yaml` rather than here. The first five run in
parallel and are blind to each other; the last two run in order.

<!-- END GENERATED agent-table -->

Mô hình nằm trong frontmatter của mỗi tác nhân, và bảng điều phối trong
`skills/adversarial-review/SKILL.md` cũng nêu tên một mô hình cho mỗi tác nhân.
Hai chỗ đó được `tests/test_structure.py` đối chiếu với nhau: frontmatter là thứ
mà một harness thực sự dựa vào để điều phối, còn cột trong bảng là tài liệu ghi
lại điều đó.

Một tác nhân không khai báo mô hình sẽ lấy bất cứ mô hình nào phiên làm việc
đang chạy. Điều đó âm thầm san phẳng một vòng đánh giá vốn cố ý trộn nhiều mức
mô hình, và đó là lý do trường này là bắt buộc chứ không phải tùy chọn.

Cách chia không tùy tiện. Các vai rẻ tiền hơn đều mô phỏng một lượt đọc **có
biên và mang tính cơ học**: mười một giây lướt qua, một bảng kiểm điều kiện, một
bộ phân tích cú pháp, sự bực bội của một người đọc đã mệt. Đó là những nhiệm vụ
được đặc tả rõ, nơi một mô hình lớn hơn chủ yếu chỉ thêm chi phí.

Các vai đắt tiền đều đòi hỏi **ước lượng một thứ không có trong tài liệu**.
Chuyên viên phân tích nhóm ứng viên phải mô tả những ứng viên không hề nằm trước
mặt nó. Quản lý tuyển dụng phải cân năm bản báo cáo với nhau rồi cho ra các xác
suất. Người phản biện phải dựng lên lập luận mạnh nhất rằng tất cả những thứ
trên đều sai. Những việc đó suy giảm thấy rõ trên một mô hình nhỏ hơn, và chúng
là ba vai mà bạn thực sự hành động theo đầu ra.

## Đặt tiền tố không gian tên

Mọi tác nhân của quy trình đều mang tiền tố `slushpile-` để nó không thể va vào
một tác nhân bạn đã có sẵn. Một người dùng đã có `contrarian` của riêng mình thì
vẫn giữ nó; tác nhân của quy trình này là `slushpile-contrarian` và hai bên
không bao giờ gặp nhau.

## Tác nhân giọng văn là ngoại lệ có chủ ý

Tác nhân giọng văn là tác nhân duy nhất trong kho mã này không mang tên
`slushpile-*`, và là tác nhân duy nhất mang tên của một con người.

Đó là vì nó được sinh ra cho từng người bởi
[written-voice-replication](https://github.com/aaddrick/written-voice-replication)
và được đặt tên theo tác giả của nó. Một người dùng thay bằng tác nhân của chính
mình phải giữ được cái tên đó, nên cái tên được đọc từ `preferences.yaml` lúc
chạy chứ không nằm cứng ở đâu cả:

```yaml
voice:
  agent: "your-name-voice"
  is_mine: true
```

`agents/aaddrick-voice.md` được phát hành như ví dụ công khai đã chạy được của
quy trình đó, để slushpile chạy được ngay từ đầu trước khi bạn kịp sinh ra tác
nhân của mình. Đó là giọng của tác giả plugin, không phải giọng của bạn, và
chừng nào `is_mine` còn là false thì mọi kỹ năng có soạn văn xuôi đều cảnh báo
trước khi chạy. Cảnh báo đó là thứ duy nhất đứng giữa bạn và mười hai hồ sơ được
gửi đi bằng giọng của một người lạ.

Nó được miễn trừ khỏi các mẫu nhận dạng danh tính trong
`scripts/check_no_pii.py`, nhưng không bao giờ được miễn trừ khỏi mẫu về thông
tin liên hệ. Xem [personal-data.md](personal-data.md).

**Đừng thêm một tác nhân giọng văn thứ hai vào kho mã này.** Một ví dụ là một
bản demo; hai ví dụ là một thư viện giọng của người khác mà chẳng ai yêu cầu.
