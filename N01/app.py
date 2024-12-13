import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import re

def preprocess_text(text):
    # Bước 1: Làm sạch
    text = text.replace("\n", " ")
    text = re.sub(r"[i|r|k|d]\)", "-", text)
    text = re.sub(r"ng\.\.\.", "v.v.", text)
    text = " ".join(text.split())

    # Bước 2: Tái cấu trúc
    text = text.replace("1.", "1. ").replace("2.", "2. ")
    text = text.replace(";", "; ").replace("-", "- ")

    return text



# -----------------------------------
# Cấu hình ứng dụng
# -----------------------------------

# Tên mô hình trên HuggingFace
HF_MODEL_NAME = "Lusic/testmodel"

# Các tham số cấu hình cho việc sinh văn bản
MAX_NEW_TOKENS = 256  # Số lượng token tối đa sinh ra
TEMPERATURE = 1.5  # Độ ngẫu nhiên trong việc sinh văn bản
TOP_P = 0.9  # Giá trị xác suất tích lũy (top-p sampling)

# Kiểm tra và chọn thiết bị (GPU nếu có, nếu không sử dụng CPU)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# -----------------------------------
# Khởi tạo mô hình và tokenizer
# -----------------------------------

@st.cache_resource
def initialize_model_and_tokenizer(model_name):
    """
    Hàm này tải mô hình và tokenizer từ HuggingFace.
    Sau khi tải, mô hình sẽ được đưa đến thiết bị tương ứng (GPU hoặc CPU).
    """
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        model.to(DEVICE)
        model.eval()
        return tokenizer, model

    except Exception as e:
        # Thông báo lỗi nếu không tải được mô hình hoặc tokenizer
        st.error(f"Lỗi khi tải mô hình hoặc tokenizer: {e}")
        st.stop()

# Khởi tạo tokenizer và model
tokenizer, model = initialize_model_and_tokenizer(HF_MODEL_NAME='Lusic/testmodel')

# -----------------------------------
# Giao diện Streamlit
# -----------------------------------

# Tiêu đề của ứng dụng
st.title("🤖 Ứng Dụng Chat với Mô Hình Ngôn Ngữ")

# Mô tả ứng dụng
st.markdown(
    """
    Chào mừng bạn đến với ứng dụng Chat AI! Ứng dụng này cho phép bạn tương tác với
    mô hình ngôn ngữ **Lusic/testmodel** từ HuggingFace. Hãy nhập tin nhắn bên dưới và nhận phản hồi từ AI.
    """
)

# Nhập tin nhắn của người dùng
user_input = st.text_area("📝 Tin nhắn của bạn:", height=150, placeholder="Nhập nội dung tin nhắn tại đây...")
if st.button("💬 Tạo phản hồi"):
    if user_input.strip() == "":  # Kiểm tra nếu người dùng chưa nhập nội dung
        st.warning("Vui lòng nhập tin nhắn để nhận phản hồi.")
    else:
        with st.spinner("🔄 Đang sinh phản hồi..."):
            try:
                messages = [
                    {"role": "user", "content": user_input}
                ]

                # Chuyển tin nhắn thành input cho mô hình (dùng tokenizer)
                inputs = tokenizer.apply_chat_template(
                    messages,
                    tokenize=True,
                    add_generation_prompt=True,  
                    return_tensors="pt",
                ).to(DEVICE)

                # Sinh phản hồi từ mô hình
                outputs = model.generate(
                    input_ids=inputs,
                    max_new_tokens=MAX_NEW_TOKENS,
                    use_cache=True,
                    temperature=TEMPERATURE,
                    top_p=TOP_P,
                )

                response = tokenizer.batch_decode(outputs, skip_special_tokens=True)

                st.success("🗨️ **Phản hồi từ mô hình:**")
                st.write(preprocess_text(response[0]))

            except Exception as e:
                st.error(f"Lỗi khi tạo phản hồi: {e}")

# -----------------------------------
# Sidebar với hướng dẫn sử dụng
# -----------------------------------

# Sidebar chứa thông tin hướng dẫn
st.sidebar.header("📖 Hướng dẫn sử dụng")
st.sidebar.info(
    """
- **Nhập tin nhắn của bạn:** Gõ nội dung tin nhắn vào ô văn bản.
- **Tạo phản hồi:** Nhấn nút "Tạo phản hồi" để nhận câu trả lời từ mô hình.
- **Chi tiết mô hình:** Ứng dụng sử dụng mô hình HuggingFace [Lusic/testmodel](https://huggingface.co/Lusic/testmodel).
- **Yêu cầu hệ thống:** Khuyến nghị chạy trên máy tính có GPU để đạt hiệu suất cao nhất.
- **Lưu ý:** Đảm bảo các thư viện cần thiết đã được cài đặt.
    """
)

# -----------------------------------
# Footer
# -----------------------------------

# Phần ghi chú dưới cùng của ứng dụng
st.markdown(
    """
    ---
    🛠️ **Phát triển bởi Streamlit** | 📅 **Ngày:** 8 Tháng 12, 2024
    """
)
