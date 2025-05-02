

otp_msg = """Hi {fname} {lname}!!,

We are pleased to welcome you to Aaradhya group. Your OTP for registration is "{otp}".

Please enter this OTP to complete your registration.

*** Please do not share this OTP with anyone ***

Thanks & Regards,
Aaradhya group
"""

welcome_msg = """Dear {student.first_name} {student.last_name}!!,  #{student.id}

Your QR code is generated. Please find the attachment below. 

Your account details are:
Email: {student.email}
Password: {student.password}

*** Please keep your password safe and do not share with anyone ***

Thanks & Regards,
Aaradhya group
"""

forgot_password_msg = """Hi {profile.first_name} {profile.last_name}!!, \n\n
Your password is: "{profile.password}" \n\n
Please keep it secure. \n\n
Thanks & Regards, \n
Aaradhya Group \
 """


fees_paid_msg = """Dear {profile.first_name} {profile.last_name}!! #{profile.id}

!!!! Greetings From Aaradhya Group !!!

This is to confirm that we have received your full payment for the Garba class fees. Thank you 
for completing the payment!!

We look forward to seeing you in class and hope you have a great time learning and dancing.

Payment description is as follow:

Payable amount :  "{profile.fees_amount}/-"
Paid amount : "{profile.fees_paid}/-"
Current Fees status : "Paid successfully"

Payment marked by: {student.first_name} {student.last_name}

You can save this email as your fees receipt.

*** Please check your fees status in your I-Card. It will be turn blue. If not then contact your admin ***

Best Regards,
Aaradhya Group
"""

aadhar_verified_msg = """Dear {student.first_name} {student.last_name}!! #{student.id}

!!!! Greetings From Aaradhya Group !!!

Your Aadhaar card has been successfully verified for your enrollment in the Garba class. We have 
completed the verification process and everything is in order.

You are all set to continue attending the classes without any issues. If you have any further 
questions or need assistance, please feel free to reach out to us.

Aadhaar Card verified by:- {viewer.first_name} {viewer.last_name}

*** Please check your Aadhaar card status in your I-Card. It will be turn blue. If not then contact your admin ***

Best Regards,
Aaradhya Group
"""

unverified_accounts_warning_msg = """Dear Student,

It has come to our notice that your account setup is still incomplete. We kindly request you to complete your account setup at the earliest to avoid any inconvenience.

Note: Unverified accounts will be locked OR deleted after 3 days.

Best Regards,
Aaradhya Group
"""

fees_reminder_msg = """Dear Student,

We would like to remind you that your Garba class fees is still pending. 

We kindly request you to complete the payment at your earliest convenience.

Note: ***Late payments may incur additional charges.***

Best Regards,
Aaradhya Group
"""