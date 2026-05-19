import streamlit as st
import stack

st.title("Stack")

if 'stack' not in st.session_state:
    st.session_state.stack = stack.stack()

col1, col2 = st.columns(2)

with col1:
    st.header("Push")
    data = st.number_input("Masukkan data untuk push", value=0)
    if st.button("Push"):
        st.session_state.stack.push(data)
        st.success(f"Data {data} berhasil ditambahkan ke stack")

with col2:
    st.header("Pop")
    if st.button("Pop"):
        popped_data = st.session_state.stack.pop()
        if popped_data is not None:
            st.success(f"Data {popped_data} berhasil dihapus dari stack")
            