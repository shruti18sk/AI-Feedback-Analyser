import streamlit as st
import requests

from database import save_analysis, get_recent_analyses


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Feedback Analyzer",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)


API_URL = "http://127.0.0.1:8000/analyze"


# =========================================================
# SESSION STATE
# =========================================================

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "review" not in st.session_state:
    st.session_state.review = ""

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False


# =========================================================
# THEME
# =========================================================

dark = st.session_state.dark_mode

if dark:
    BG = "#0d1024"
    CARD = "#151936"
    TEXT = "#f7f5ff"
    MUTED = "#a8abc7"
    BORDER = "#30365a"
    PURPLE = "#9879e8"
    LIGHT_PURPLE = "#241d45"
    INPUT = "#11162d"

else:
    BG = "#faf9f7"
    CARD = "#ffffff"
    TEXT = "#191733"
    MUTED = "#858397"
    BORDER = "#e5e0eb"
    PURPLE = "#7654d8"
    LIGHT_PURPLE = "#f1ebff"
    INPUT = "#ffffff"


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    f"""
    <style>

    .stApp {{
        background: {BG};
        color: {TEXT};
    }}

    .block-container {{
        max-width: 1180px;
        padding-top: 1.5rem;
        padding-bottom: 4rem;
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    /* ---------------- LOGO ---------------- */

    .logo {{
        font-family: Georgia, serif;
        font-size: 30px;
        font-weight: 700;
        color: {TEXT};
    }}

    .logo-star {{
        color: {PURPLE};
    }}

    .logo-dot {{
        color: {PURPLE};
    }}

    .logo-sub {{
        color: {MUTED};
        font-size: 9px;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        margin-top: 2px;
    }}

    .profile {{
        text-align: right;
        color: {TEXT};
        font-size: 13px;
        font-weight: 700;
        padding-top: 10px;
    }}

    /* ---------------- HERO ---------------- */

    .hero {{
        background: linear-gradient(
            135deg,
            {CARD},
            {LIGHT_PURPLE}
        );

        border: 1px solid {BORDER};
        border-radius: 25px;
        padding: 42px;
        min-height: 300px;

        display: flex;
        flex-direction: column;
        justify-content: center;

        box-shadow: 0 15px 40px rgba(80, 60, 130, 0.08);
    }}

    .hero-badge {{
        display: inline-block;
        width: fit-content;

        background: {CARD};
        color: {PURPLE};

        border: 1px solid {BORDER};
        border-radius: 999px;

        padding: 7px 13px;

        font-size: 9px;
        font-weight: 800;
        letter-spacing: 1px;
        text-transform: uppercase;

        margin-bottom: 16px;
    }}

    .main-title {{
        font-family: Georgia, serif;
        font-size: 52px;
        font-weight: 700;
        line-height: 1.05;
        letter-spacing: -2px;
        color: {TEXT};
    }}

    .main-title span {{
        color: {PURPLE};
        font-style: italic;
    }}

    .subtitle {{
        color: {MUTED};
        font-size: 14px;
        line-height: 1.7;
        margin-top: 12px;
    }}

    .hero-mini {{
        background: {CARD};

        border: 1px solid {BORDER};
        border-radius: 25px;

        min-height: 300px;
        padding: 30px;

        display: flex;
        align-items: center;
        justify-content: center;

        text-align: center;

        box-shadow: 0 15px 40px rgba(80, 60, 130, 0.08);
    }}

    .hero-icon {{
        width: 70px;
        height: 70px;

        margin: auto auto 17px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 21px;

        background: {LIGHT_PURPLE};
        color: {PURPLE};

        font-size: 32px;
    }}

    .hero-mini-title {{
        color: {TEXT};
        font-size: 15px;
        font-weight: 800;
    }}

    .hero-mini-text {{
        color: {MUTED};
        font-size: 11px;
        line-height: 1.8;
        margin-top: 8px;
    }}

    /* ---------------- LABELS ---------------- */

    .small-label {{
        color: {PURPLE};
        font-size: 9px;
        font-weight: 800;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }}

    .section-title {{
        font-family: Georgia, serif;
        font-size: 30px;
        font-weight: 700;
        color: {TEXT};
        margin-top: 3px;
    }}

    .section-description {{
        color: {MUTED};
        font-size: 12px;
        margin-top: 4px;
    }}

    .input-title {{
        color: {TEXT};
        font-size: 14px;
        font-weight: 800;
        margin-top: 28px;
        margin-bottom: 8px;
    }}

    /* ---------------- TEXT AREA ---------------- */

    textarea {{
        background: {INPUT} !important;
        color: {TEXT} !important;

        border: 1px solid {BORDER} !important;
        border-radius: 16px !important;

        font-size: 14px !important;
        line-height: 1.6 !important;
    }}

    textarea:focus {{
        border-color: {PURPLE} !important;

        box-shadow:
            0 0 0 2px rgba(118, 84, 216, 0.12) !important;
    }}

    textarea::placeholder {{
        color: {MUTED} !important;
    }}

    /* ---------------- BUTTON ---------------- */

    .stButton button {{
        border: none !important;
        border-radius: 14px !important;

        min-height: 48px !important;

        background:
            linear-gradient(
                135deg,
                #211f40,
                #7654d8
            ) !important;

        color: white !important;

        font-weight: 800 !important;
        font-size: 13px !important;

        transition: 0.2s ease !important;
    }}

    .stButton button:hover {{
        transform: translateY(-2px);
    }}

    /* ---------------- ANALYSIS CARDS ---------------- */

    .card {{
        background: {CARD};

        border: 1px solid {BORDER};
        border-radius: 19px;

        min-height: 285px;
        padding: 22px;

        box-shadow:
            0 8px 25px rgba(80, 60, 130, 0.07);
    }}

    .card-label {{
        color: {MUTED};

        font-size: 9px;
        font-weight: 800;

        letter-spacing: 1.4px;
        text-transform: uppercase;
    }}

    /* ---------------- SENTIMENT ---------------- */

    .sentiment-icon {{
        width: 65px;
        height: 65px;

        border-radius: 50%;

        display: flex;
        align-items: center;
        justify-content: center;

        margin: 28px auto 12px;

        font-size: 34px;
    }}

    .sentiment-name {{
        text-align: center;

        font-family: Georgia, serif;

        font-size: 34px;
        font-weight: 700;
    }}

    .sentiment-note {{
        margin-top: 38px;

        text-align: center;

        padding: 10px;

        border-radius: 999px;

        font-size: 10px;
        font-weight: 800;
    }}

    /* ---------------- SCORE ---------------- */

    .score {{
        text-align: center;

        margin-top: 30px;

        font-family: Georgia, serif;

        font-size: 58px;
        font-weight: 700;

        color: {TEXT};
    }}

    .score span {{
        font-family: Arial, sans-serif;

        color: {MUTED};

        font-size: 14px;
        font-weight: 400;
    }}

    .stars {{
        text-align: center;

        color: {PURPLE};

        font-size: 23px;

        letter-spacing: 3px;

        margin-top: 4px;
    }}

    .score-note {{
        margin-top: 42px;

        text-align: center;

        background: {LIGHT_PURPLE};
        color: {PURPLE};

        padding: 10px;

        border-radius: 999px;

        font-size: 10px;
        font-weight: 800;
    }}

    /* ---------------- CONFIDENCE ---------------- */

    .confidence-number {{
        text-align: center;

        font-family: Georgia, serif;

        font-size: 45px;
        font-weight: 700;

        color: {TEXT};

        margin-top: 45px;
    }}

    .confidence-bar {{
        height: 12px;
        width: 100%;

        border-radius: 999px;

        background: {LIGHT_PURPLE};

        margin-top: 20px;

        overflow: hidden;
    }}

    .confidence-fill {{
        height: 100%;

        border-radius: 999px;

        background:
            linear-gradient(
                90deg,
                #e95a62,
                #f2c94c,
                #20aa70
            );
    }}

    .confidence-label {{
        text-align: center;

        color: {PURPLE};

        font-size: 10px;
        font-weight: 800;

        margin-top: 13px;
    }}

    /* ---------------- STATUS ---------------- */

    .status-icon {{
        width: 65px;
        height: 65px;

        border-radius: 50%;

        display: flex;
        align-items: center;
        justify-content: center;

        margin: 28px auto 12px;

        background: #e9f8ef;
        color: #20a765;

        font-size: 30px;
    }}

    .status-name {{
        text-align: center;

        font-family: Georgia, serif;

        font-size: 31px;
        font-weight: 700;

        color: #20a765;
    }}

    .status-note {{
        margin-top: 38px;

        text-align: center;

        padding: 10px;

        border-radius: 999px;

        background: #e9f8ef;
        color: #15975b;

        font-size: 10px;
        font-weight: 800;
    }}

    /* ---------------- INSIGHT ---------------- */

    .insight {{
        background:
            linear-gradient(
                110deg,
                {CARD},
                {LIGHT_PURPLE}
            );

        border: 1px solid {BORDER};

        border-radius: 19px;

        padding: 23px 25px;

        margin-top: 20px;

        box-shadow:
            0 8px 25px rgba(80, 60, 130, 0.07);
    }}

    .insight-label {{
        color: {PURPLE};

        font-size: 9px;
        font-weight: 800;

        letter-spacing: 1.4px;
        text-transform: uppercase;
    }}

    .insight-text {{
        color: {TEXT};

        font-size: 14px;
        line-height: 1.7;

        margin-top: 10px;

        padding-right: 45px;
    }}

    /* ---------------- LOWER CARDS ---------------- */

    .lower {{
        background: {CARD};

        border: 1px solid {BORDER};

        border-radius: 19px;

        min-height: 145px;

        padding: 22px;

        box-shadow:
            0 8px 25px rgba(80, 60, 130, 0.07);
    }}

    .theme {{
        color: {PURPLE};

        font-family: Georgia, serif;

        font-size: 31px;
        font-weight: 700;

        margin-top: 15px;
    }}

    .lower-description {{
        color: {MUTED};

        font-size: 10px;

        margin-top: 3px;
    }}

    .keyword {{
        display: inline-block;

        background: {LIGHT_PURPLE};

        border: 1px solid {BORDER};

        color: {PURPLE};

        border-radius: 999px;

        padding: 7px 12px;

        margin: 15px 5px 0 0;

        font-size: 10px;
        font-weight: 800;
    }}

    /* ---------------- HISTORY ---------------- */

    .history {{
        background: {CARD};

        border: 1px solid {BORDER};

        border-radius: 17px;

        padding: 17px 20px;

        margin-bottom: 10px;

        box-shadow:
            0 6px 20px rgba(80, 60, 130, 0.06);
    }}

    .history-review {{
        color: {TEXT};

        font-size: 13px;
        line-height: 1.6;

        margin-top: 10px;
    }}

    .history-info {{
        color: {MUTED};

        font-size: 10px;
    }}

    .badge {{
        display: inline-block;

        border-radius: 999px;

        padding: 6px 10px;

        font-size: 9px;
        font-weight: 800;
    }}

    .positive-badge {{
        color: #15975b;
        background: #e9f8ef;
    }}

    .negative-badge {{
        color: #d84c58;
        background: #fff0f1;
    }}

    .neutral-badge {{
        color: #bd8124;
        background: #fff7e6;
    }}

    /* ---------------- MOBILE ---------------- */

    @media (max-width: 800px) {{

        .main-title {{
            font-size: 40px;
        }}

        .hero {{
            padding: 30px;
        }}

    }}

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

header_left, header_right = st.columns([3, 1])


with header_left:

    st.html(
        """
        <div class="logo">
            <span class="logo-star">✦</span>
            feedback<span class="logo-dot">.</span>
        </div>

        <div class="logo-sub">
            Customer Feedback Analyzer
        </div>
        """
    )


with header_right:

    st.html(
        """
        <div class="profile">
            Feedback Dashboard
        </div>
        """
    )

    if st.button(
        "☀ Light" if dark else "☾ Dark",
        use_container_width=True
    ):
        st.session_state.dark_mode = not dark
        st.rerun()


st.divider()


# =========================================================
# HERO SECTION
# =========================================================

hero1, hero2 = st.columns(
    [1.8, 0.8],
    gap="medium"
)


with hero1:

    st.html(
        """
        <div class="hero">

            <div class="hero-badge">
                ✦ AI-powered customer intelligence
            </div>

            <div class="main-title">
                Turn feedback<br>
                into <span>insight.</span>
            </div>

            <div class="subtitle">
                Understand what customers love, what needs
                attention, and what your reviews are really
                telling you.
            </div>

        </div>
        """
    )


with hero2:

    st.html(
        """
        <div class="hero-mini">

            <div>

                <div class="hero-icon">
                    ✦
                </div>

                <div class="hero-mini-title">
                    From words to clarity
                </div>

                <div class="hero-mini-text">
                    Sentiment · Score · Theme<br>
                    Confidence · Status · Insight
                </div>

            </div>

        </div>
        """
    )


# =========================================================
# FEEDBACK INPUT
# =========================================================

st.html(
    """
    <div class="input-title">
        ✎ &nbsp; Enter Customer Feedback
    </div>
    """
)


review_text = st.text_area(
    "Feedback",
    value=st.session_state.review,
    placeholder="Write or paste customer feedback here...",
    height=145,
    max_chars=500,
    label_visibility="collapsed"
)


st.caption(
    f"{len(review_text)} / 500 characters"
)


# =========================================================
# ANALYZE BUTTON
# =========================================================

if st.button(
    "✦  Analyze Feedback",
    use_container_width=True
):

    if not review_text.strip():

        st.warning(
            "Please enter customer feedback first."
        )

    else:

        with st.spinner(
            "Analyzing your feedback..."
        ):

            try:

                response = requests.post(
                    API_URL,
                    json={
                        "text": review_text.strip()
                    },
                    timeout=60
                )

                response.raise_for_status()

                analysis = response.json()

                st.session_state.analysis = analysis
                st.session_state.review = review_text.strip()

                save_analysis(
                    review_text.strip(),
                    analysis
                )

                st.success(
                    "Analysis complete ✦"
                )

            except requests.exceptions.ConnectionError:

                st.error(
                    "FastAPI is not running. "
                    "Start it with: uvicorn api:app --reload"
                )

            except requests.exceptions.Timeout:

                st.error(
                    "Request timed out. Please try again."
                )

            except requests.exceptions.HTTPError as e:

                st.error(
                    f"API error: {e}"
                )

            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )


# =========================================================
# ANALYSIS RESULT
# =========================================================

if st.session_state.analysis:

    analysis = st.session_state.analysis


    # -----------------------------------------------------
    # SAFE DATA EXTRACTION
    # -----------------------------------------------------

    sentiment = str(
        analysis.get(
            "sentiment",
            "neutral"
        )
    ).lower()


    try:

        score = int(
            analysis.get(
                "score",
                3
            )
        )

    except (ValueError, TypeError):

        score = 3


    score = max(
        1,
        min(
            5,
            score
        )
    )


    theme = str(
        analysis.get(
            "theme",
            "General"
        )
    )


    try:

        confidence = int(
            analysis.get(
                "confidence",
                0
            )
        )

    except (ValueError, TypeError):

        confidence = 0


    confidence = max(
        0,
        min(
            100,
            confidence
        )
    )


    status = str(
        analysis.get(
            "status",
            "Follow Up"
        )
    )


    insight = str(
        analysis.get(
            "insight",
            "No additional insight available."
        )
    )


    keywords = analysis.get(
        "keywords",
        []
    )


    if not isinstance(
        keywords,
        list
    ):

        keywords = [
            str(keywords)
        ]


    # -----------------------------------------------------
    # SENTIMENT UI
    # -----------------------------------------------------

    if sentiment == "positive":

        sentiment_icon = "☺"
        sentiment_color = "#20a765"
        sentiment_bg = "#e9f8ef"
        sentiment_note = "Customer is happy"

    elif sentiment == "negative":

        sentiment_icon = "☹"
        sentiment_color = "#e35c67"
        sentiment_bg = "#fff0f1"
        sentiment_note = "Customer needs attention"

    else:

        sentiment_icon = "•"
        sentiment_color = "#c28b2c"
        sentiment_bg = "#fff7e6"
        sentiment_note = "Mixed or neutral feedback"


    # -----------------------------------------------------
    # SCORE UI
    # -----------------------------------------------------

    score_labels = {
        1: "Very Poor",
        2: "Needs Improvement",
        3: "Average",
        4: "Good",
        5: "Excellent"
    }


    score_text = score_labels.get(
        score,
        "Rated"
    )


    stars = (
        "★" * score
        +
        "☆" * (5 - score)
    )


    # -----------------------------------------------------
    # CONFIDENCE UI
    # -----------------------------------------------------

    if confidence >= 80:

        confidence_text = "Very High Confidence"

    elif confidence >= 50:

        confidence_text = "Moderate Confidence"

    else:

        confidence_text = "Low Confidence"


    # -----------------------------------------------------
    # STATUS UI
    # -----------------------------------------------------

    status_display = (
        status
        .replace(
            "_",
            " "
        )
        .title()
    )


    status_lower = status.lower()


    if status_lower == "satisfied":

        status_note = "Customer appears happy"

    elif status_lower == "resolved":

        status_note = "Issue appears resolved"

    else:

        status_note = "May need follow-up"


    # =====================================================
    # RESULT HEADING
    # =====================================================

    st.write("")
    st.write("")


    st.html(
        """
        <div class="small-label">
            Analysis complete
        </div>

        <div class="section-title">
            Here's what the review says ✧
        </div>

        <div class="section-description">
            A clear snapshot of what your customer is telling you.
        </div>
        """
    )


    st.write("")


    # =====================================================
    # FOUR ANALYSIS CARDS
    # =====================================================

    c1, c2, c3, c4 = st.columns(
        4,
        gap="medium"
    )


    # -----------------------------------------------------
    # SENTIMENT CARD
    # -----------------------------------------------------

    with c1:

        st.html(
            f"""
            <div class="card">

                <div class="card-label">
                    Sentiment
                </div>

                <div
                    class="sentiment-icon"
                    style="
                        background:{sentiment_bg};
                        color:{sentiment_color};
                    "
                >
                    {sentiment_icon}
                </div>

                <div
                    class="sentiment-name"
                    style="
                        color:{sentiment_color};
                    "
                >
                    {sentiment.title()}
                </div>

                <div
                    class="sentiment-note"
                    style="
                        background:{sentiment_bg};
                        color:{sentiment_color};
                    "
                >
                    ● &nbsp; {sentiment_note}
                </div>

            </div>
            """
        )


    # -----------------------------------------------------
    # SCORE CARD
    # -----------------------------------------------------

    with c2:

        st.html(
            f"""
            <div class="card">

                <div class="card-label">
                    Satisfaction Score
                </div>

                <div class="score">
                    {score}
                    <span>/ 5</span>
                </div>

                <div class="stars">
                    {stars}
                </div>

                <div class="score-note">
                    {score_text}
                </div>

            </div>
            """
        )


    # -----------------------------------------------------
    # CONFIDENCE CARD
    # -----------------------------------------------------

    with c3:

        st.html(
            f"""
            <div class="card">

                <div class="card-label">
                    Confidence Level
                </div>

                <div class="confidence-number">
                    {confidence}%
                </div>

                <div class="confidence-bar">

                    <div
                        class="confidence-fill"
                        style="
                            width:{confidence}%;
                        "
                    ></div>

                </div>

                <div class="confidence-label">
                    {confidence_text}
                </div>

            </div>
            """
        )


    # -----------------------------------------------------
    # STATUS CARD
    # -----------------------------------------------------

    with c4:

        st.html(
            f"""
            <div class="card">

                <div class="card-label">
                    Status
                </div>

                <div class="status-icon">
                    ✓
                </div>

                <div class="status-name">
                    {status_display}
                </div>

                <div class="status-note">
                    {status_note}
                </div>

            </div>
            """
        )


    # =====================================================
    # AI INSIGHT
    # =====================================================

    st.html(
        f"""
        <div class="insight">

            <div class="insight-label">
                ✦ &nbsp; AI Insight
            </div>

            <div class="insight-text">
                {insight}
            </div>

        </div>
        """
    )


    st.write("")


    # =====================================================
    # THEME + KEYWORDS
    # =====================================================

    theme_col, keywords_col = st.columns(
        2,
        gap="medium"
    )


    # -----------------------------------------------------
    # THEME
    # -----------------------------------------------------

    with theme_col:

        st.html(
            f"""
            <div class="lower">

                <div class="card-label">
                    Main Theme
                </div>

                <div class="theme">
                    {theme.title()}
                </div>

                <div class="lower-description">
                    Main topic detected from the review
                </div>

            </div>
            """
        )


    # -----------------------------------------------------
    # KEYWORDS
    # -----------------------------------------------------

    with keywords_col:

        keyword_html = ""


        for keyword in keywords:

            keyword_html += (
                f'<span class="keyword">'
                f'{str(keyword)}'
                f'</span>'
            )


        if not keyword_html:

            keyword_html = (
                '<span class="lower-description">'
                'No keywords detected'
                '</span>'
            )


        st.html(
            f"""
            <div class="lower">

                <div class="card-label">
                    Keywords
                </div>

                <div>
                    {keyword_html}
                </div>

            </div>
            """
        )


# =========================================================
# RECENT HISTORY
# =========================================================

try:

    recent = get_recent_analyses(
        limit=5
    )

except Exception:

    recent = []


if recent:

    st.write("")
    st.write("")
    st.write("")


    # -----------------------------------------------------
    # HISTORY HEADER
    # -----------------------------------------------------

    st.html(
        """
        <div class="small-label">
            History
        </div>

        <div class="section-title">
            Recent Analyses
        </div>

        <div class="section-description">
            Your latest customer feedback insights.
        </div>
        """
    )


    st.write("")


    # -----------------------------------------------------
    # HISTORY ITEMS
    # -----------------------------------------------------

    for row in recent:

        try:

            review = str(
                row[1]
            )

            history_sentiment = str(
                row[2]
            )

            history_score = row[3]

            history_theme = str(
                row[4]
            )

            history_status = str(
                row[6]
            )

            created_at = str(
                row[9]
            )

        except Exception:

            continue


        # Limit review length

        if len(review) > 180:

            review = (
                review[:180]
                +
                "..."
            )


        # Badge class

        if history_sentiment.lower() == "positive":

            badge_class = "positive-badge"

        elif history_sentiment.lower() == "negative":

            badge_class = "negative-badge"

        else:

            badge_class = "neutral-badge"


        # -------------------------------------------------
        # HISTORY CARD
        # -------------------------------------------------

        st.html(
            f"""
            <div class="history">

                <div>

                    <span class="badge {badge_class}">
                        {history_sentiment.title()}
                    </span>

                    <span class="history-info">
                        &nbsp; {history_score}/5
                    </span>

                    <span class="history-info">
                        &nbsp; • &nbsp;
                        {history_theme.title()}
                    </span>

                    <span class="history-info">
                        &nbsp; • &nbsp;
                        {history_status.replace("_", " ").title()}
                    </span>

                    <span class="history-info">
                        &nbsp; • &nbsp;
                        {created_at}
                    </span>

                </div>

                <div class="history-review">
                    “{review}”
                </div>

            </div>
            """
        )