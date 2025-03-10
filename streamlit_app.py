import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("📄 Document question answering")
st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.secrets["OPENAI_API_KEY"]
document = ""
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    option = st.selectbox(
    "Choose your data?",
        ("Shoes Online Store", "Upload your own data"),
    )

    

    if (option == "Upload your own data"):

        # Let the user upload a file via `st.file_uploader`.
        uploaded_file = st.file_uploader(
            "Upload a document (.txt or .md)", type=("txt", "md")
        )

        if uploaded_file:
            # Process the uploaded file and question.
            document = uploaded_file.read().decode()


    if (option == "Shoes Online Store"):
        document = """ 
Shoes eCommerce Store - Question & Answer Knowledgebase

1. Orders & Payments

Q1: How do I place an order?

A: Simply browse our website, select your desired shoes, choose the correct size, and click "Add to Cart." Proceed to checkout, enter your shipping and payment details, and confirm your order.

Q2: What payment methods do you accept?

A: We accept major credit and debit cards (Visa, MasterCard, American Express), PayPal, Apple Pay, Google Pay, and Afterpay (where applicable).

Q3: Can I cancel or modify my order after placing it?

A: Yes, you can modify or cancel your order within 24 hours of placing it. Contact our support team as soon as possible for assistance.

Q4: How do I use a discount code?

A: At checkout, enter your discount code in the designated field and click "Apply." The discount will be reflected in your total order amount.

2. Shipping & Delivery

Q5: What are the shipping options and delivery times?

A: We offer the following shipping options:

Standard Shipping: 5-7 business days

Express Shipping: 2-3 business days

Overnight Shipping: Next-day delivery (order before 2 PM)

International Shipping: 7-14 business days (varies by country)

Q6: How do I track my order?

A: Once your order is shipped, you will receive a tracking number via email. You can use this number to track your order on our website or the carrier's website.

Q7: Do you offer free shipping?

A: Yes! We offer free standard shipping on orders over $100 within the U.S. International shipping rates may vary.

Q8: What should I do if my order is delayed?

A: If your order is delayed beyond the estimated delivery time, please contact our customer support team, and we will investigate the issue.

3. Returns & Exchanges

Q9: What is your return policy?

A: We accept returns within 30 days of purchase. Shoes must be unworn, in their original packaging, and include all accessories. Return shipping is free for domestic orders.

Q10: How do I initiate a return or exchange?

A: Log into your account, navigate to "My Orders," select the item you want to return, and follow the instructions. You will receive a return label via email.

Q11: Can I exchange my shoes for a different size or style?

A: Yes, we offer free exchanges for a different size or style within 30 days. If the desired product is unavailable, you can request store credit or a refund.

Q12: How long does it take to process a refund?

A: Refunds are typically processed within 5-7 business days after we receive and inspect your returned item.

4. Product Information & Sizing

Q13: How do I choose the right size?

A: We provide a detailed size chart on each product page. If you are unsure, refer to our sizing guide or contact support for assistance.

Q14: Do you offer wide or narrow width shoes?

A: Yes, we offer various width options for select styles. Look for "Wide" or "Narrow" in the product description.

Q15: Are your shoes true to size?

A: Most of our shoes fit true to size. However, we recommend reading customer reviews for additional fit information.

Q16: What materials are your shoes made from?

A: Our shoes are made from high-quality materials, including genuine leather, synthetic materials, suede, mesh, and eco-friendly options. Product details are available on each product page.

5. Account & Support

Q17: Do I need an account to place an order?

A: No, you can check out as a guest. However, creating an account allows you to track orders, save shipping details, and receive exclusive offers.

Q18: How do I reset my password?

A: Click "Forgot Password" on the login page, enter your email, and follow the instructions sent to your inbox.

Q19: How can I contact customer support?

A: You can reach our support team via email at support@shoestore.com, through our live chat, or by calling our toll-free number at (800) 123-4567.

Q20: Do you offer gift cards?

A: Yes! You can purchase digital or physical gift cards ranging from $25 to $200.

6. Promotions & Loyalty Program

Q21: Do you have a rewards program?

A: Yes! Join our rewards program to earn points on every purchase, which can be redeemed for discounts on future orders.

Q22: How do I sign up for exclusive offers?

A: Subscribe to our newsletter for early access to sales, special promotions, and new arrivals.

Q23: Can I refer a friend and get a discount?

A: Yes! Refer a friend, and both of you will receive a $10 discount on your next purchase.
"""


    # Ask the user for a question via `st.text_area`.
    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not document,
    )

    
    if document and question: 
        messages = [
            {
                "role": "system",
                "content": f"You'll help to answer a customer question based on the provided document, do not answer any question that is outside the scope of the document.",
            },
            {
                "role": "user",
                "content": f"Here's a document: {document} \n\n---\n\n {question}",
            }
        ]

        # Generate an answer using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            stream=True,
        )

        # Stream the response to the app using `st.write_stream`.
        st.write_stream(stream)
