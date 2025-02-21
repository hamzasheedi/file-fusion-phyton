import streamlit as st
import pandas as pd
import os
from io import BytesIO
from PIL import Image  


st.set_page_config(page_title="File Fusion", layout='wide')


#buffer and mime
buffer = BytesIO()
mime_type = "application/octet-stream"  

#guide
st.info("HOW TO USE FILE FUSION..!!!")
st.write("""  
### 🔥 **Welcome to File Fusion!**  
This app allows you to easily manage your files:  

✅ **Supported File Types:** CSV, Excel, Text, PDF, Images (PNG, JPG, WEBP)  
✅ **Features:**  
    -  **Preview Files** before processing  
    -  **Clean Data** (Remove duplicates, Fill missing values)  
    -  **Convert Files** (CSV ↔ Excel, Image Format Change)  
    -  **Data Visualization** (Quick Charts)  
    -  **Download Processed Files**  

🔹 **Steps to Use:**  
1 **Upload your file**  
2 **Preview & clean data** (if applicable)  
3 **Convert file to desired format**  
4 **Visualize the data**  
5 **Download your processed file**  

🚀 Get started by uploading your file above!  
""")
st.success("🎯 Tip: Expand this section anytime for guidance!")

# Title / Description
st.title("File Fusion")
st.markdown("### One Tool for All Your File Needs.")

#style
st.markdown(
    """
    <style>
    .stApp {
        background-color: purple ;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

#hooks
st.info("📂 Drop your files here or click to upload",)


# File Uploader
uploaded_files = st.file_uploader(
    "📂",
    type=["csv", "xlsx", "txt", "pdf", "jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True
)

# Process Uploaded Files
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        df = None  
        new_file_name = file.name  

        # Read file extension
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue

        
        # File Info
        st.success(f"✅ **Uploaded:** {file.name} ({file.size} bytes)")

        #only for CSV and Excel
        if df is not None:
            #tabs of csv and excel
            preview_tab, dataCleaning_tab, conversion_tab, visual_tab, download_tab = st.tabs(
                ["Preview", "Data Cleaning", "File Conversion", "Visualization", "Download"]
            )

            with preview_tab:
                st.write(" **Preview of Data**")
                st.dataframe(df.head())

            # Data Cleaning
            with dataCleaning_tab:
                st.subheader(" Data Cleaning")
                if st.checkbox(f"Clean Data for **{file.name}**"):
                    col1, col2 = st.columns(2)

                    with col1:
                        if st.checkbox(" Remove Duplicates"):
                            df.drop_duplicates(inplace=True)
                            st.write("✅ **Duplicates Removed!**")

                    with col2:
                        if st.checkbox(" Fill Missing Values"):
                            numeric_cols = df.select_dtypes(include=['number']).columns
                            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                            st.write("✅ **Missing values filled with column mean!**")


            with conversion_tab:
                st.subheader("📌 Select Columns")
                columns = st.multiselect(
                    f"^ Deselect the columns you want to remove from the file. **{file.name}**", 
                    df.columns, 
                    default=df.columns
                )
                df = df[columns]


                if st.checkbox(f"🔄 Convert File: {file.name}"):
                    conversion_options = ["CSV", "Excel"]
                    conversion_type = st.radio(f"Choose conversion format for **{file.name}**:", conversion_options)

                    if st.button(f"Convert {file.name} to {conversion_type}"):
                        new_file_name = os.path.splitext(file.name)[0] + f".{conversion_type.lower()}"


                        if conversion_type == "CSV":
                            df.to_csv(buffer, index=False)
                            mime_type = "text/csv"

                        elif conversion_type == "Excel":
                            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                                df.to_excel(writer, index=False)
                            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

                        buffer.seek(0)


                        st.success("✅ Your file has been successfully converted! You can now download it from the 'Download' tab. 🚀")

            with visual_tab:
                st.subheader("📊 Quick Visualization")
                if st.checkbox(f"📉 Show Chart for **{file.name}**"):
                    st.bar_chart(df.select_dtypes(include=['number']).iloc[:, :2])


            with download_tab:
                if buffer.getvalue():
                    st.download_button(
                        label="📥 Download Converted File",
                        data=buffer.getvalue(),
                        file_name=new_file_name,
                        mime=mime_type
                    )
                    st.success("Thanks You For Using File Fusion")

                else:
                    st.download_button(
                        label="📥 Download Original File",
                        data=file.read(),
                        file_name=new_file_name,
                        mime="application/octet-stream"
                    )
                    st.success("Thanks You For Using File Fusion")

        # FOR IMAGE FILES
        elif file_ext in [".png", ".jpg", ".jpeg", ".webp"]:
            preview_tab, conversion_tab, download_tab = st.tabs(["Preview", "File Conversion", "Download"])

            with preview_tab:
                img = Image.open(file)
                st.image(img, caption="Preview of Uploaded Image", use_column_width=True)
                width, height = img.size
                st.write(f"📏 **Image Dimensions:** {width} x {height} pixels")
                st.write(f"🖼️ **Image Format:** {img.format}")

            with conversion_tab:
                conversion_options = ["PNG", "JPEG", "WEBP"]
                conversion_type = st.radio("Convert Image To:", conversion_options)

                if st.button(f"Convert to {conversion_type}"):
                    buffer = BytesIO()
                    img.save(buffer, format=conversion_type)
                    buffer.seek(0)
                    mime_type = f"image/{conversion_type.lower()}"
                    st.success(f"✅ Image converted to {conversion_type} successfully!")

            with download_tab:
                if buffer.getvalue():
                    st.download_button("📥 Download Edited Image", buffer, file_name="converted_image.png", mime=mime_type)
                    st.success("Thanks You For Using File Fusion")
