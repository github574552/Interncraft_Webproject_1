# Interncraft_Webproject_1
1. Time Management
 Ensure you adhere strictly to the deadlines. Timeliness is crucial.
2. Proper Documentation
 Along with your project submission, prepare and submit proper documentation 
detailing your project. This documentation should include:
o Project Overview: A brief description of your project.
o Objectives: The main goals and objectives of your project.
o Methodology: The approach and methods you used to complete the project.
o Challenges: Any challenges or hurdles you faced and how you overcame 
them.
o Conclusion: The final outcome and any recommendations or future steps.
3. Originality
 Your project must be original and not copied from any source. Plagiarism will result in 
the cancellation of your project submission.
Note
 Regularly update your LinkedIn profile with your progress and achievements, as it is 
crucial for your career.
Project Title: eCommerce Website
Submission Date :- 13/09/2024
Page 1: Introduction
1.1. Purpose
The purpose of this document is to outline the software requirements for the full-stack 
development of an eCommerce website. The project is designed to provide interns with 
hands-on experience in building a fully functional eCommerce platform.
1.2. Scope
This SRS covers the front-end, back-end, database management, and API development 
aspects of the project. The website will enable users to browse products, manage a shopping 
cart, and complete purchases.
1.3. Definitions, Acronyms, and Abbreviations
 API: Application Programming Interface
 CRUD: Create, Read, Update, Delete
 JWT: JSON Web Token
 UI: User Interface
1.4. References
 Web Standards: W3C, WCAG 2.1
 Security Guidelines: OWASP Top Ten
1.5. Overview
This document details the functional and non-functional requirements, design constraints, and 
assumptions for the eCommerce website.
Page 3: Functional Requirements
3.1. Home Page
 Purpose: Provide a welcoming interface with navigation to key sections.
 Features:
o Display featured products, offers, and a search bar.
o Include navigation links to product categories, user login, and cart.
3.2. User Authentication
 Purpose: Allow users to register, log in, and manage their profiles.
 Features:
o User registration with email verification.
o Login functionality using JWT.
o Password recovery through email.
3.3. Product Browsing
 Purpose: Enable users to view and search for products.
 Features:
o Product listing by categories with sorting and filtering options.
o Detailed product page with images, descriptions, price, and stock 
information.
o User reviews and ratings.
3.4. Shopping Cart
 Purpose: Allow users to manage selected products before purchasing.
 Features:
o Add to cart functionality from the product page.
o View, update quantities, and remove items from the cart.
o Persistent cart across sessions for logged-in users.
3.5. Checkout Process
 Purpose: Facilitate the purchase of products in the cart.
 Features:
o Collection of shipping information.
o Selection of payment method.
o Order review and confirmation.
3.6. Payment Integration
 Purpose: Process payments securely.
 Features:
o Integration with a payment gateway like Stripe or PayPal.
o Secure handling of payment details.
o Display of transaction confirmation.
3.7. Order Management
 Purpose: Manage user orders and track their status.
 Features:
o Order summary page with details of purchased items.
o Order history page for users to view past purchases.
o Order tracking feature for users to monitor delivery status.
3.8. Admin Product Management
 Purpose: Allow admins to manage the product inventory.
 Features:
o CRUD operations for products, including adding new items, editing existing 
ones, and removing out-of-stock items.
o Inventory tracking and management.
o Category management for organizing products.
3.9. User Profile Management
 Purpose: Allow users to manage their personal information and view order history.
 Features:
o Profile update functionality for name, email, and shipping address.
o View past orders and download receipts.
o Manage saved payment methods.
Page 6: Non-Functional Requirements
4.1. Performance
 The website should be responsive and load pages within 3 seconds under normal 
conditions.
4.2. Security
 Implement HTTPS for secure communication.
 Use JWT for secure user authentication.
 Implement input validation to protect against security threats like SQL injection, XSS, 
and CSRF.
4.3. Usability
 The UI should be user-friendly, with a clear navigation structure.
 Ensure accessibility compliance with WCAG 2.1 guidelines for users with disabilities.
4.4. Scalability
 The system should be designed to handle increased traffic and data without 
significant changes to the architecture.
4.5. Reliability
 The website should have a high availability rate of 99.9%, with robust error handling
and recovery processes.
