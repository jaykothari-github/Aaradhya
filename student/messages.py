

otp_msg = """Hi {fname} {lname}!!,

We are pleased to welcome you to Aaradhya group. Your OTP for registration is "{otp}".

Please enter this OTP to complete your registration.

*** Please do not share this OTP with anyone ***

Thanks & Regards,
Aaradhya group
"""

welcome_msg = """Hi {student.first_name} {student.last_name}!!,

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


fees_paid_msg = """Hi {profile.first_name} {profile.last_name}!! #{profile.id}

!!!! Greetings From Aaradhya Group !!!

This is to confirm that we have received your full payment for the Garba class fees. Thank you 
for completing the payment!!

We look forward to seeing you in class and hope you have a great time learning and dancing.

Payment description is as follow:

Your payable amount :  "{profile.fees_amount}/-"
Your paid amount : "{profile.fees_paid}/-"
Current Fees status : "Paid successfully"

You can save this email as your fees receipt.

*** Please check your fees status in your I-Card. It will be turn blue. If not then contact your admin ***

Best Regards,
Aaradhya Group
"""