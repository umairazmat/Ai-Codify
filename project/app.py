import streamlit as st
from openai_client import get_code_review_response, refactor_code


def main():
    st.title("CodeMentor - (AI-Enhanced Code Collaboration Tool)")
    st.subheader("Collaborate, Refactor, and Optimize with AI.")
    st.write(
        "A smart tool for distributed teams to automate code reviews, refactor efficiently, and get real-time AI-driven feedback."
    )

    # Instructions
    st.write(
        "Upload a file or paste your code below to get an AI-generated code review."
    )

    # Input Methods: File Upload or Text Area
    uploaded_file = st.file_uploader(
        "Upload a code file (Max 500 lines)", type=["py", "js", "txt"]
    )
    code_input = st.text_area("Or paste your code here (Max 1000 words)", height=300)

    # Limit input size for code
    if uploaded_file:
        code = uploaded_file.read().decode("utf-8")
        if len(code.splitlines()) > 500:
            st.error(
                "File is too large! Please upload a file with a maximum of 500 lines."
            )
            code = None  # Reset code if it's too large
        else:
            st.success(f"File uploaded: {uploaded_file.name}")
    elif code_input:
        code = code_input
        if len(code.split()) > 1000:
            st.error("Code exceeds 1000 words! Please shorten your code.")
            code = None  # Reset code if it's too large
    else:
        code = None

    # Button to trigger code review
    if st.button("Get Code Review") and code:
        with st.spinner("Processing..."):
            # Call the OpenAI API to get code review
            review = get_code_review_response(code)
            st.subheader("Code Review Results:")
            st.write(review)

            # Provide download option
            st.download_button(
                label="Download Code Review",
                data=review,
                file_name="code_review.txt",
                mime="text/plain",
            )
            st.success("You can download the code review as code_review.txt")

        # Button to trigger code refactoring
    if st.button("Refactor Code") and code:
        with st.spinner("Refactoring your code..."):
            refactored_code = refactor_code(code)
            st.subheader("Refactored Code:")
            st.write(refactored_code)

            # Provide download option for refactored code
            st.download_button(
                label="Download Refactored Code",
                data=refactored_code,
                file_name="refactored_code.txt",
                mime="text/plain",
            )
            st.success("You can download the refactored code as refactored_code.txt")


if __name__ == "__main__":
    main()
