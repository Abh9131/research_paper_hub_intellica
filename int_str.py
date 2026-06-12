import streamlit as st
import arxiv
from langchain_core.documents import Document

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Intellica",
    page_icon="📚",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #0a192f 0%,
        #112240 50%,
        #1b2a49 100%
    );
}

/* Hide Streamlit menu */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* Title */
.main-title {
    text-align: center;
    font-size: 70px;
    font-weight: 800;
    color: #64ffda;
    margin-top: 20px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #ccd6f6;
    font-size: 24px;
    margin-bottom: 10px;
}

/* Description */
.description {
    text-align: center;
    color: #8892b0;
    font-size: 18px;
    margin-bottom: 40px;
}

/* Paper Card */
.paper-card {
    background-color: rgba(17, 34, 64, 0.95);
    padding: 25px;
    border-radius: 20px;
    margin-bottom: 25px;
    border: 1px solid #233554;
    transition: all 0.3s ease;
}

.paper-card:hover {
    border: 1px solid #64ffda;
}

.paper-title {
    color: #64ffda;
    font-size: 26px;
    font-weight: bold;
}

.paper-meta {
    color: #8892b0;
    margin-top: 8px;
}

.paper-summary {
    color: white;
    margin-top: 15px;
    line-height: 1.8;
}

.result-header {
    color: white;
    font-size: 30px;
    margin-top: 30px;
    margin-bottom: 25px;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">Intellica</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-Powered Research Discovery</div>',
    unsafe_allow_html=True
)

st.markdown(
    '''
    <div class="description">
    Search academic papers from Intellica and discover the latest breakthroughs
    in Artificial Intelligence, Data Science, Physics, Mathematics and more.
    </div>
    ''',
    unsafe_allow_html=True
)

# --------------------------------------------------
# SEARCH SECTION
# --------------------------------------------------

col1, col2, col3 = st.columns([1, 3, 1])

with col2:

    topic = st.text_input(
        "",
        placeholder="🔍 Enter a research topic (e.g. Deep Learning)"
    )

    max_results = st.number_input(
    "Number of Articles",
    min_value=1,
    max_value=100,
    value=5,
    step=1
)

    search_button = st.button(
        "🚀 Search Papers",
        use_container_width=True
    )

# --------------------------------------------------
# WELCOME SCREEN
# --------------------------------------------------

if not search_button:

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.info(
        """
        👋 Welcome to Intellica

        Enter a research topic above and discover cutting-edge academic papers from Intellica.

        Examples:
        • Large Language Models
        • Generative AI
        • Computer Vision
        • Reinforcement Learning
        • Data Science
        • Quantum Computing
        • Cyber Security
        """
    )

# --------------------------------------------------
# SEARCH RESULTS
# --------------------------------------------------

if search_button:

    if topic.strip() == "":
        st.warning("Please enter a research topic.")
        st.stop()

    docs = []

    with st.spinner("Searching papers..."):

        try:

            client = arxiv.Client()

            search = arxiv.Search(
                query=topic,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )

            for paper in client.results(search):

                docs.append(
                    Document(
                        page_content=paper.summary,
                        metadata={
                            "title": paper.title,
                            "url": paper.entry_id,
                            "pdf": paper.pdf_url,
                            "published": str(
                                paper.published.date()
                            ),
                            "authors": ", ".join(
                                [author.name for author in paper.authors]
                            )
                        }
                    )
                )

        except Exception as e:
            st.error(f"Error: {e}")
            st.stop()

    # --------------------------------------------------
    # RESULTS HEADER
    # --------------------------------------------------

    st.markdown(
        f"""
        <div class="result-header">
        📚 Found {len(docs)} Papers for "{topic}"
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------

    for i, doc in enumerate(docs, start=1):

        st.markdown(
            f"""
            <div class="paper-card">

            <div class="paper-title">
            {i}. {doc.metadata['title']}
            </div>

            <div class="paper-meta">
            👨‍🔬 Authors: {doc.metadata['authors']}
            </div>

            <div class="paper-meta">
            📅 Published: {doc.metadata['published']}
            </div>

            <div class="paper-summary">
            {doc.page_content[:800]}...
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        c1, c2 = st.columns(2)

        with c1:
            st.link_button(
                "📖 Read Paper",
                doc.metadata["url"],
                use_container_width=True
            )

        with c2:
            st.link_button(
                "📥 Download PDF",
                doc.metadata["pdf"],
                use_container_width=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <hr style="border:1px solid #233554">

    <center style="color:#8892b0">
    Built By Abhishek
    </center>
    """,
    unsafe_allow_html=True
)
