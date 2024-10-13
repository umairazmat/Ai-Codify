import streamlit as st
from openai_client import (
    get_code_review_response,
    refactor_code,
    code_feedback,
    suggest_best_practices,
    remove_code_errors,
)


def main():
    # Title and Description
    st.title("CodeMentor")
    st.write(
        "A smart tool for distributed teams to automate code reviews, refactor efficiently, and get real-time AI-driven feedback."
    )

    # Main Features Section
    st.write("### Main Features:")
    st.write(
        """
        - **Code Review**: Get AI-generated reviews to improve your code.
        - **Code Refactoring**: Automatically refactor your code for better readability and efficiency.
        - **Code Feedback**: Real-time feedback on code quality and potential improvements.
        - **Best Practices Suggestions**: AI-driven suggestions tailored to your specific code.
        - **Error Removal**: Identify and suggest fixes for errors in your code.
        - **Downloadable Results**: Download reviews, refactored code, feedback, best practices, and error suggestions as text files.
        """
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

    # Button to trigger code feedback
    if st.button("Get Code Feedback") and code:
        with st.spinner("Getting feedback on your code..."):
            feedback = code_feedback(code)
            st.subheader("Code Feedback:")
            st.write(feedback)

            # Ensure feedback is a string for download
            feedback_text = feedback if isinstance(feedback, str) else str(feedback)

            # Provide download option for code feedback
            st.download_button(
                label="Download Code Feedback",
                data=feedback_text,  # Use the extracted string here
                file_name="code_feedback.txt",
                mime="text/plain",
            )
            st.success("You can download the code feedback as code_feedback.txt")

    # Add button to suggest best practices
    if st.button("Suggest Best Practices") and code:
        with st.spinner("Getting best practices..."):
            best_practices = suggest_best_practices(code)
            st.subheader("Best Practices Suggestions:")
            st.write(best_practices)

            # Provide download option for best practices suggestions
            best_practices_text = (
                best_practices
                if isinstance(best_practices, str)
                else str(best_practices)
            )
            st.download_button(
                label="Download Best Practices Suggestions",
                data=best_practices_text,
                file_name="best_practices.txt",
                mime="text/plain",
            )
            st.success(
                "You can download the best practices suggestions as best_practices.txt"
            )

    # Button to trigger error removal
    if st.button("Remove Code Errors") and code:
        with st.spinner("Removing errors from your code..."):
            error_removal_suggestions = remove_code_errors(code)
            st.subheader("Error Removal Suggestions:")
            st.write(error_removal_suggestions)

            # Provide download option for error removal suggestions
            error_removal_text = (
                error_removal_suggestions
                if isinstance(error_removal_suggestions, str)
                else str(error_removal_suggestions)
            )
            st.download_button(
                label="Download Error Removal Suggestions",
                data=error_removal_text,
                file_name="error_removal_suggestions.txt",
                mime="text/plain",
            )
            st.success(
                "You can download the error removal suggestions as error_removal_suggestions.txt"
            )


if __name__ == "__main__":
    main()
