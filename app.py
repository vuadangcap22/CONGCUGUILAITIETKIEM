import streamlit as st
st.image("logo.jpg")
import pandas as pd
import math

# =========================
# CẤU HÌNH TRANG
# =========================

st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

st.title("💰 TÍNH LÃI GỬI TIẾT KIỆM")
st.write("Nhập thông tin khoản tiền gửi để tính tiền lãi và tổng số tiền nhận được.")

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================

def format_vnd(value):
    return f"{value:,.0f} VNĐ".replace(",", ".")


# =========================
# NHẬP DỮ LIỆU
# =========================

st.subheader("📌 Thông tin khoản tiền gửi")

tien_gui = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=100_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

ky_han = st.number_input(
    "Kỳ hạn (tháng)",
    min_value=1,
    max_value=120,
    value=12,
    step=1
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=5.0,
    step=0.1,
    format="%.2f"
)

hinh_thuc_nhan_lai = st.selectbox(
    "Hình thức nhận lãi",
    [
        "Cuối kỳ",
        "Hàng tháng",
        "Hàng quý"
    ]
)

loai_lai = st.selectbox(
    "Phương pháp tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ]
)

# =========================
# TÍNH TOÁN
# =========================

if st.button("🧮 TÍNH LÃI", use_container_width=True):

    if tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0%.")
        st.stop()

    # Lãi suất theo tháng
    lai_suat_nam = lai_suat / 100
    lai_suat_thang = lai_suat_nam / 12

    # Xác định số tháng giữa các lần nhận lãi
    if hinh_thuc_nhan_lai == "Hàng tháng":
        so_thang_moi_ky = 1
    elif hinh_thuc_nhan_lai == "Hàng quý":
        so_thang_moi_ky = 3
    else:
        so_thang_moi_ky = ky_han

    # Số kỳ nhận lãi
    so_ky = math.ceil(ky_han / so_thang_moi_ky)

    # =========================
    # LÃI ĐƠN
    # =========================

    if loai_lai == "Lãi đơn":

        # Với lãi đơn:
        # Tiền lãi mỗi tháng = Gốc × lãi suất năm / 12
        lai_moi_thang = tien_gui * lai_suat_thang

        tong_lai = tien_gui * lai_suat_nam * (ky_han / 12)

        # Tạo bảng chi tiết
        danh_sach = []

        for ky in range(1, so_ky + 1):

            thang_bat_dau = (ky - 1) * so_thang_moi_ky + 1
            thang_ket_thuc = min(ky * so_thang_moi_ky, ky_han)

            so_thang_thuc_te = thang_ket_thuc - thang_bat_dau + 1

            lai_ky = tien_gui * lai_suat_thang * so_thang_thuc_te

            danh_sach.append({
                "Kỳ": ky,
                "Thời gian": f"Tháng {thang_bat_dau} - {thang_ket_thuc}",
                "Tiền gốc": tien_gui,
                "Tiền lãi kỳ này": lai_ky,
                "Tổng nhận": tien_gui + lai_ky
            })

    # =========================
    # LÃI KÉP
    # =========================

    else:

        danh_sach = []
        so_du = tien_gui
        tong_lai = 0

        # Lãi kép được nhập vào vốn sau mỗi kỳ nhận lãi.
        # Nếu nhận lãi cuối kỳ thì toàn bộ kỳ hạn được tính
        # như một lần ghép lãi.

        if hinh_thuc_nhan_lai == "Cuối kỳ":

            so_ky = 1

            # Lãi kép theo số tháng
            tong_tien = tien_gui * (
                1 + lai_suat_nam
            ) ** (ky_han / 12)

            tong_lai = tong_tien - tien_gui

            danh_sach.append({
                "Kỳ": 1,
                "Thời gian": f"{ky_han} tháng",
                "Tiền gốc": tien_gui,
                "Tiền lãi kỳ này": tong_lai,
                "Tổng nhận": tong_tien
            })

        else:

            tong_lai = 0

            for ky in range(1, so_ky + 1):

                thang_bat_dau = (ky - 1) * so_thang_moi_ky + 1
                thang_ket_thuc = min(
                    ky * so_thang_moi_ky,
                    ky_han
                )

                so_thang_thuc_te = (
                    thang_ket_thuc - thang_bat_dau + 1
                )

                # Lãi suất tương ứng với số tháng của kỳ
                lai_ky = so_du * (
                    (1 + lai_suat_thang) ** so_thang_thuc_te - 1
                )

                tong_lai += lai_ky
                so_du += lai_ky

                danh_sach.append({
                    "Kỳ": ky,
                    "Thời gian": f"Tháng {thang_bat_dau} - {thang_ket_thuc}",
                    "Tiền gốc đầu kỳ": so_du - lai_ky,
                    "Tiền lãi kỳ này": lai_ky,
                    "Tổng nhận": so_du
                })

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================

    tong_tien = tien_gui + tong_lai

    st.success("✅ Đã tính toán xong!")

    st.subheader("📊 Kết quả")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Tiền lãi định kỳ",
            format_vnd(
                danh_sach[0]["Tiền lãi kỳ này"]
            )
        )

    with col2:
        st.metric(
            "Tổng tiền lãi",
            format_vnd(tong_lai)
        )

    with col3:
        st.metric(
            "Tổng gốc + lãi",
            format_vnd(tong_tien)
        )

    # =========================
    # THÔNG TIN TÓM TẮT
    # =========================

    st.subheader("📋 Tóm tắt khoản gửi")

    st.write(
        f"**Số tiền gửi:** {format_vnd(tien_gui)}"
    )

    st.write(
        f"**Kỳ hạn:** {ky_han} tháng"
    )

    st.write(
        f"**Lãi suất:** {lai_suat:.2f}%/năm"
    )

    st.write(
        f"**Hình thức nhận lãi:** {hinh_thuc_nhan_lai}"
    )

    st.write(
        f"**Phương pháp:** {loai_lai}"
    )

    # =========================
    # BẢNG CHI TIẾT
    # =========================

    st.subheader("📅 Chi tiết tiền lãi")

    df = pd.DataFrame(danh_sach)

    # Format các cột tiền
    for column in df.columns:
        if "Tiền" in column or "Tổng nhận" in column:
            df[column] = df[column].apply(format_vnd)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # =========================
    # LƯU Ý
    # =========================

    st.info(
        "💡 Kết quả trên là mô phỏng theo lãi suất cố định do người dùng nhập. "
        "Thực tế ngân hàng có thể áp dụng cách tính lãi, ngày tính lãi, "
        "quy định tất toán trước hạn và phương thức nhập lãi khác nhau."
    )
