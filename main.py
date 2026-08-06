import os
from pathlib import Path


# Указываем локальную директорию с моделями до импорта rembg.
MODEL_DIR = Path(__file__).resolve().parent / "models"
os.environ["U2NET_HOME"] = str(MODEL_DIR)

import streamlit as st
from rembg import new_session, remove


st.set_page_config(
    page_title="Удаление фона с изображения",
)

description = {
    "isnet-general-use": {
        "Режим": "Быстрый",
        "Особенности": "Хорошее качество при меньшей задержке",
        "Лучше использовать": (
            "Обычные фотографии с хорошо различимым объектом переднего плана"
        ),
    },
    "u2net": {
        "Режим": "Классический",
        "Особенности": "Проверенная модель общего назначения",
        "Лучше использовать": (
            "Простые сцены с одним заметным объектом и несложными границами"
        ),
    },
    "u2netp": {
        "Режим": "Сверхлёгкий",
        "Особенности": "Минимальный размер и низкие требования к ресурсам",
        "Лучше использовать": (
            "Быстрое превью, слабые устройства и изображения с простым объектом"
        ),
    },
}

MODELS = list(description)
DEFAULT_MODEL = "isnet-general-use"


@st.cache_resource(
    max_entries=1,
    show_spinner="Загружаем модель...",
)
def load_model(name: str):
    return new_session(name)


st.title("Удаление фона с изображения")
st.write(
    "Загрузите фотографию, выберите подходящую модель и скачайте результат "
    "с прозрачным фоном. Модели отличаются качеством обработки границ, "
    "скоростью и требованиями к ресурсам."
)

with st.expander("Как выбрать модель", expanded=True):
    st.table(
        [
            {"Модель": model, **description[model]}
            for model in MODELS
        ]
    )

model_name = st.selectbox(
    "Выберите модель",
    MODELS,
    index=MODELS.index(DEFAULT_MODEL),
)

selected_model = description[model_name]
st.info(
    f"**{selected_model['Режим']} режим.** "
    f"{selected_model['Особенности']}. "
    f"{selected_model['Лучше использовать']}."
)

session = load_model(model_name)


uploaded_file = st.file_uploader(
    "Загрузите изображение",
    type=["png", "jpg", "jpeg"],
)

if uploaded_file is not None:
    with st.spinner("Удаляем фон с изображения...", show_time=True):
        result = remove(uploaded_file.getvalue(), session=session)

    st.image(result, caption=f"Результат: {model_name}")
    st.download_button(
        "Скачать результат",
        data=result,
        file_name="result.png",
        mime="image/png",
    )
