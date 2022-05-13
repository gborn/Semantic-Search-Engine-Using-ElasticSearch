
import streamlit as st
from typing import List
import requests
import json

def get_results(query:str, k:int, n:int) -> List[dict]:
    url = f"https://8erilhfztj.execute-api.ap-south-1.amazonaws.com/semantic-search-api-stage/query?query={query}&n={n}&k={k}"
    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    results_ = json.loads(response.text)
    results = [{
        'title': result['_source']['title'],
        'body': result['_source']['body'],
        'score': result['_score']
    } for result in results_]

    return results


def main():
    """
    Main driver program for streamlit that renders UI and connects to API Gateway backend
    """
    st.title('Semantic Search Engine')

    query = None
    results = None
    query = st.text_input('Enter Search Query:')
    k = st.sidebar.slider("Choose K (Nearest Neighbors):", value=1, min_value=1, max_value=10, step=1)
    n = st.sidebar.slider("Number of results to display", value=10, min_value=5, max_value=30, step=5)

    if query:
            with st.spinner(f'Getting Results for {query}'):
                results = get_results(query, k, n)

                if not results:
                    st.text('No search results found')

                st.subheader('Results')
                for result in results:
                    with st.expander(result['title']):
                        st.markdown(result['body'], unsafe_allow_html=True)

                results = None


if __name__ == '__main__':
    main()