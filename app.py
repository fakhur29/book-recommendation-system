import pickle 
import streamlit as st
import numpy as np 





st.header("Book recommender system")
model = pickle.load(open('artifacts/model.pkl' , 'rb'))
svd = pickle.load(open('artifacts/svd.pkl', 'rb'))
books_name  = pickle.load(open('artifacts/books_name.pkl' , 'rb'))
final_rating = pickle.load(open('artifacts/final_rating.pkl' , 'rb'))
book_pivot  = pickle.load(open('artifacts/book_pivot.pkl' , 'rb'))



def fecth_poster(suggestion):
    book_name = []
    ids_index = []
    poster_url = []

    for book_id in suggestion:
        book_name.append(book_pivot.index[book_id])

    for name in book_name[0]:
        ids = np.where(final_rating['title']==name)[0][0]
        ids_index.append(ids)
    for idx in ids_index:
        url = final_rating.iloc[idx]['img_url']
        poster_url.append(url)
    return poster_url

def recommend_book(book_name):
    book_list = []
    book_id = np.where(book_pivot.index == book_name)[0][0]
    book_vector = svd.transform(book_pivot.iloc[book_id, :].values.reshape(1, -1))
    distance, suggestion = model.kneighbors(book_vector, n_neighbors=6)

    poster_url = fecth_poster(suggestion)

    for i in range(len(suggestion)):
        books = book_pivot.index[suggestion[i]]
        for j in books:
            book_list.append(j)
    return book_list,poster_url


selected_books = st.selectbox(
    "Select a book",
    books_name
)

if st.button("Show Recommendations"):
    recommenddation_book, poster_url = recommend_book(selected_books)

    cols = st.columns(5)

    for i, col in enumerate(cols, start=1):
        with col:
            st.image(poster_url[i], width=150)
            st.markdown(f"<p style='text-align:center; font-size:14px; height:40px;'>{recommenddation_book[i]}</p>", unsafe_allow_html=True)
