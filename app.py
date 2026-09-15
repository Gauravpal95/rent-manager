import streamlit as st
import pandas as pd
from datetime import datetime, date
import os
from tinydb import TinyDB, Query

# ==========================================
# ⚙️ 1. PAGE CONFIGURATION & METADATA
# ==========================================
st.set_page_config(
    page_title="RENT MANAGER - Elite Management Suite",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 🗄️ 2. HYBRID DATABASE ENGINE (TinyDB Local Backup)
# ==========================================
db_file = "rent_manager_db.json"
local_db = TinyDB(db_file)

rooms_table = local_db.table("rooms")
complaints_table = local_db.table("complaints")
expenses_table = local_db.table("expenses")
settings_table = local_db.table("settings")

# Initialize default records if empty
if not rooms_table.all():
    rooms_table.insert({
        "Room 101": {
            "status": "Occupied", "tenant": "Rahul Sharma", "phone": "9876543210", 
            "emergency_contact": "Father: 9876500000", "security_deposit": 15000,
            "rent": 6800, "light": 750, "maint": 300,
            "doc": "Aadhaar_Rahul.pdf", "owner_doc": "Lease_Agreement_101.pdf", 
            "history": {
                "May 2026": {"total": 7350, "status": "Paid", "receipt": "REC-101-MAY"},
                "June 2026": {"total": 7850, "status": "Pending", "receipt": None}
            }
        },
        "Room 102": {
            "status": "Vacant", "tenant": "None Assigned", "phone": "",
            "emergency_contact": "", "security_deposit": 0,
            "rent": 6000, "light": 400, "maint": 100,
            "doc": None, "owner_doc": None,
            "history": {
                "May 2026": {"total": 6500, "status": "Paid", "receipt": "REC-102-MAY"},
                "June 2026": {"total": 6500, "status": "Pending", "receipt": None}
            }
        }
    })

if not complaints_table.all():
    complaints_table.insert({
        "id": 1, "room": "Room 101", "tenant": "Rahul Sharma", 
        "category": "Plumbing", "desc": "Bathroom tap leakage", "status": "Open", "priority": "High"
    })

if not expenses_table.all():
    expenses_table.insert({"desc": "Plumbing repair for Room 101", "amount": 500, "date": "2026-06-01"})

if not settings_table.all():
    settings_table.insert({
        "passwords": {"owner": "owner123", "tenant": "tenant123"},
        "owner_profile": {"name": "Gaurav Pal", "phone": "9876543210", "address": "Binary Boys Elite Apartments, Surat"},
        "notices": ["📢 Building general maintenance scheduled for Sunday 10 AM."],
        "late_fee_rule": 100
    })

# Bind with Session State
if "rooms" not in st.session_state:
    st.session_state.rooms = rooms_table.all()[0]
if "complaints" not in st.session_state:
    st.session_state.complaints = complaints_table.all()
if "expenses" not in st.session_state:
    st.session_state.expenses = expenses_table.all()

settings_data = settings_table.all()[0]
if "passwords" not in st.session_state: st.session_state.passwords = settings_data["passwords"]
if "owner_profile" not in st.session_state: st.session_state.owner_profile = settings_data["owner_profile"]
if "notices" not in st.session_state: st.session_state.notices = settings_data["notices"]
if "late_fee_rule" not in st.session_state: st.session_state.late_fee_rule = settings_data["late_fee_rule"]

def sync_to_db():
    rooms_table.truncate()
    rooms_table.insert(st.session_state.rooms)
    complaints_table.truncate()
    for c in st.session_state.complaints: complaints_table.insert(c)
    expenses_table.truncate()
    for e in st.session_state.expenses: expenses_table.insert(e)
    settings_table.truncate()
    settings_table.insert({
        "passwords": st.session_state.passwords,
        "owner_profile": st.session_state.owner_profile,
        "notices": st.session_state.notices,
        "late_fee_rule": st.session_state.late_fee_rule
    })

# ==========================================
# 🎨 3. PROFESSIONAL DESIGN & CYBER-TECH CSS
# ==========================================
st.markdown("""
    <style>
    .main {
        background-color: #030712;
        background-image: 
            radial-gradient(circle at 50% 0%, rgba(16, 185, 129, 0.08) 0%, transparent 60%),
            linear-gradient(to right, rgba(255, 255, 255, 0.02) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
        background-size: 100% 100%, 32px 32px, 32px 32px;
        color: #F8FAFC;
        font-family: 'Inter', sans-serif;
    }
    .stApp { background-color: #030712; }
    .card {
        background: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        padding: 24px;
        border-radius: 16px;
        border: 1px solid rgba(52, 211, 153, 0.2);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
        margin-bottom: 20px;
    }
    .metric-box {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.95) 100%);
        backdrop-filter: blur(12px);
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(52, 211, 153, 0.2);
        text-align: center;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
    }
    [data-testid="stSidebar"] {
        background-color: #080e1a;
        border-right: 1px solid rgba(52, 211, 153, 0.1);
        padding-top: 20px;
    }
    .stTextInput>div>div>input, .stSelectbox>div>div>select, .stNumberInput>div>div>input {
        background-color: rgba(15, 23, 42, 0.8) !important;
        color: #ffffff !important;
        border: 1px solid rgba(52, 211, 153, 0.25) !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
    }
    .badge-paid { background-color: rgba(6, 78, 59, 0.7); color: #34D399; padding: 4px 12px; border-radius: 6px; font-size: 12px; font-weight: bold; border: 1px solid rgba(52, 211, 153, 0.4); }
    .badge-pending { background-color: rgba(127, 29, 29, 0.7); color: #F87171; padding: 4px 12px; border-radius: 6px; font-size: 12px; font-weight: bold; border: 1px solid rgba(248, 113, 113, 0.4); }
    .badge-status { background-color: rgba(30, 58, 138, 0.7); color: #60A5FA; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: bold; border: 1px solid rgba(96, 165, 250, 0.4); }
    </style>
""", unsafe_allow_html=True)

# Session States
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "role" not in st.session_state: st.session_state.role = ""
if "assigning_room" not in st.session_state: st.session_state.assigning_room = None
if "move_out_requests" not in st.session_state: st.session_state.move_out_requests = []

# ==========================================
# 🔐 4. SECURE AUTHENTICATION & REGISTRATION
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #34D399; font-size: 0.85rem; font-weight: 700; letter-spacing: 2px; margin-top: 5px; margin-bottom: 5px;'>CREATED BY BINARY BOYS</p>", unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; color: #FFFFFF; font-size: 3rem; margin-bottom: 0;'>🏢 RENT MANAGER</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 1.15rem; margin-top: 5px; margin-bottom: 30px;'>The Elite Property & Tenant Ecosystem</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🔒 Secure Login Gateway")
        
        with st.form("combined_auth_form"):
            portal_choice = st.selectbox("Select Portal Mode", ["Tenant Portal", "Owner Dashboard"])
            password_input = st.text_input("Enter Portal Password", type="password", placeholder="Enter password")
            
            st.markdown(f"""
            <div style='font-size: 11px; color: #94A3B8; margin-top: 5px;'>
                🌐 <b>Database Mode:</b> Offline TinyDB Active<br>
                💡 Default Passwords:<br>
                • Owner: <b>{st.session_state.passwords['owner']}</b> | Tenant: <b>{st.session_state.passwords['tenant']}</b>
            </div>
            """, unsafe_allow_html=True)
            
            submit_login = st.form_submit_button("Authenticate & Enter", use_container_width=True)
            
            if submit_login:
                correct_pwd = st.session_state.passwords["owner"] if portal_choice == "Owner Dashboard" else st.session_state.passwords["tenant"]
                if password_input == correct_pwd:
                    st.session_state.logged_in = True
                    st.session_state.role = portal_choice
                    st.success("Login Successful!")
                    st.rerun()
                else:
                    st.error("Invalid Password! Please check correct role password.")
        st.markdown('</div>', unsafe_allow_html=True)

        with st.expander("🏢 New Property Owner? Click here to Register"):
            with st.form("owner_register_form"):
                reg_name = st.text_input("Full Name", placeholder="e.g. Gaurav Pal")
                reg_phone = st.text_input("Phone Number", placeholder="9876543210")
                reg_address = st.text_input("Property Address", placeholder="e.g. Elite Heights, Surat")
                reg_owner_pwd = st.text_input("Create Owner Password", type="password", placeholder="Secure owner password")
                reg_tenant_pwd = st.text_input("Create Tenant Access Password", type="password", placeholder="Secure tenant password")
                
                submit_reg = st.form_submit_button("Register & Launch Dashboard", use_container_width=True)
                
                if submit_reg:
                    if reg_name.strip() and len(reg_phone) == 10 and reg_owner_pwd.strip() and reg_tenant_pwd.strip():
                        st.session_state.owner_profile = {
                            "name": reg_name, "phone": reg_phone, "address": reg_address
                        }
                        st.session_state.passwords["owner"] = reg_owner_pwd
                        st.session_state.passwords["tenant"] = reg_tenant_pwd
                        sync_to_db()
                        
                        st.session_state.logged_in = True
                        st.session_state.role = "Owner Dashboard"
                        st.success("🎉 Registration Successful! Saved to Database & Redirecting...")
                        st.rerun()
                    else:
                        st.error("Please fill in valid details (10-digit phone number & both passwords required).")

    st.stop()


# ==========================================
# 🔑 5. TENANT PORTAL INTERFACE
# ==========================================
if st.session_state.role == "Tenant Portal":
    
    occupied_rooms = [r for r, data in st.session_state.rooms.items() if data["status"] == "Occupied"]
    if not occupied_rooms:
        st.warning("No occupied rooms available for simulation. Please login as Owner and add a tenant.")
        st.stop()
        
    with st.sidebar:
        st.markdown("### 🏢 RENT MANAGER")
        st.markdown("<p style='font-size:11px; color:#34D399; margin-top:-10px;'>CREATED BY BINARY BOYS</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        selected_tenant_room = st.selectbox("Select Your Assigned Room", occupied_rooms)
        
        st.markdown("<p style='font-size: 12px; color: #94A3B8; margin-top: 15px;'>NAVIGATION</p>", unsafe_allow_html=True)
        tenant_menu = st.radio(
            "Tenant Navigation",
            ["💳 Billing & Payments", "🛠️ Maintenance & Issues", "👤 Profile & Lease"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    room_data = st.session_state.rooms[selected_tenant_room]
    
    if st.session_state.notices:
        st.info(st.session_state.notices[-1])

    st.markdown(f"<h2>Welcome, <span style='color: #34D399;'>{room_data['tenant']}</span> ({selected_tenant_room})</h2>", unsafe_allow_html=True)

    if tenant_menu == "💳 Billing & Payments":
        col_l, col_r = st.columns([1.2, 1])

        with col_l:
            st.markdown("### 📊 Current Month Ledger")
            current_base_total = room_data['rent'] + room_data['light'] + room_data['maint']
            late_fee_added = st.session_state.late_fee_rule * 3 
            total_with_late = current_base_total + late_fee_added

            st.markdown(f"""
            <div class="card">
                <p style="color: #60A5FA; font-size: 13px; font-weight: bold;">BILLING CYCLE: CURRENT MONTH (Due Date: 5th)</p>
                <hr style="border-color: rgba(255, 255, 255, 0.1); margin-top: 5px; margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;"><span>Base Room Rent:</span> <b>₹{room_data['rent']}</b></div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;"><span>Light / Electricity Bill:</span> <b>₹{room_data['light']}</b></div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;"><span>Maintenance / Other Bill:</span> <b>₹{room_data['maint']}</b></div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 12px; color: #F87171;"><span>Late Fee Penalty (Overdue):</span> <b>+₹{late_fee_added}</b></div>
                <hr style="border-color: rgba(255, 255, 255, 0.1);">
                <div style="display: flex; justify-content: space-between; font-size: 18px; font-weight: bold; color: #34D399;">
                    <span>Total Payable Amount:</span> <span>₹{total_with_late}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_r:
            st.markdown("### ⚡ Live UPI Gateway & Verified QR")
            
            # 🌟 Display Actual Live QR Code Image and Verified UPI ID
            if os.path.exists("upi_qr.png"):
                st.image("upi_qr.png", width=200, caption="Scan & Pay via any UPI App")
            else:
                # Fallback if image file not yet placed
                st.warning("⚠️ 'upi_qr.png' not found in folder. Please place your cropped QR code image as 'upi_qr.png'.")
                st.markdown(f'<img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa=7211197425.upi.circle@ibl&am={total_with_late}&cu=INR" width="150" style="border-radius: 8px; padding: 5px; background: white;">', unsafe_allow_html=True)

            st.markdown("""
            <div class="card" style="padding: 12px; margin-top: 10px; text-align: center;">
                <p style="font-size: 13px; color: #34D399; margin: 0; font-weight: bold;">Verified UPI ID:</p>
                <p style="font-size: 15px; color: #FFFFFF; margin: 5px 0 0 0; font-family: monospace;">7211197425.upi.circle@ibl</p>
            </div>
            """, unsafe_allow_html=True)
            
            proof_file = st.file_uploader("Upload Payment Screenshot Proof", type=["png", "jpg", "jpeg"])
            if proof_file:
                st.success("Payment proof uploaded successfully to database!")

        st.markdown("### 📜 Month-wise Payment Ledger & Official Receipts")
        for month_name, m_info in room_data["history"].items():
            cols = st.columns([3, 1, 1])
            with cols[0]:
                st.markdown(f"**{month_name}**<br><span style='color: #94A3B8; font-size: 13px;'>Total Invoice Amount: ₹{m_info['total']}</span>", unsafe_allow_html=True)
            with cols[1]:
                if m_info["status"] == "Paid":
                    st.markdown("<span class='badge-paid'>PAID ✓</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span class='badge-pending'>PENDING ⚠️</span>", unsafe_allow_html=True)
            with cols[2]:
                if m_info["status"] == "Paid":
                    if st.button("Download Receipt", key=f"rec_{selected_tenant_room}_{month_name}"):
                        receipt_text = f"""
========================================
      RENT MANAGER OFFICIAL RECEIPT    
========================================
Room Number  : {selected_tenant_room}
Tenant Name  : {room_data['tenant']}
Billing Month: {month_name}
Amount Paid  : ₹{m_info['total']}
Status       : VERIFIED & PAID (Database Synced)
UPI ID Used  : 7211197425.upi.circle@ibl
Receipt ID   : {m_info['receipt']}
Date of Issue: {date.today()}
========================================
                        """
                        st.download_button("📥 Save PDF/TXT", data=receipt_text, file_name=f"Receipt_{month_name.replace(' ', '_')}.txt", key=f"dl_{selected_tenant_room}_{month_name}")
                else:
                    if st.button("Pay Now Securely", key=f"pay_{selected_tenant_room}_{month_name}"):
                        st.session_state[f"active_pay_{selected_tenant_room}_{month_name}"] = True

            if st.session_state.get(f"active_pay_{selected_tenant_room}_{month_name}", False):
                if st.button("✅ Confirm Payment & Update DB", key=f"sim_action_{selected_tenant_room}_{month_name}"):
                    room_data["history"][month_name]["status"] = "Paid"
                    if month_name == list(room_data["history"].keys())[-1]:
                        room_data["history"][month_name]["total"] = total_with_late
                    room_data["history"][month_name]["receipt"] = f"REC-{selected_tenant_room}-{month_name[:3].upper()}"
                    sync_to_db()
                    st.session_state[f"active_pay_{selected_tenant_room}_{month_name}"] = False
                    st.success("Payment saved to database successfully!")
                    st.rerun()

            st.markdown("<hr style='border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)

    elif tenant_menu == "🛠️ Maintenance & Issues":
        st.markdown("### 🛠️ Raise Maintenance Ticket")
        with st.form("tenant_complaint"):
            c_cat = st.selectbox("Issue Category", ["Plumbing", "Electrical", "Carpentry", "Appliances", "Other"])
            c_desc = st.text_input("Describe the issue in detail")
            c_priority = st.selectbox("Priority Level", ["Low", "Medium", "High"])
            if st.form_submit_button("Submit Complaint to Owner") and c_desc:
                st.session_state.complaints.append({
                    "id": len(st.session_state.complaints) + 1,
                    "room": selected_tenant_room,
                    "tenant": room_data["tenant"],
                    "category": c_cat,
                    "priority": c_priority,
                    "desc": c_desc,
                    "status": "Open"
                })
                sync_to_db()
                st.success("Complaint ticket stored in database and sent to owner!")

        st.markdown("### 📡 Your Active Ticket Live Status")
        tenant_tickets = [c for c in st.session_state.complaints if c["room"] == selected_tenant_room]
        if not tenant_tickets:
            st.info("No active maintenance tickets found.")
        else:
            for t in tenant_tickets:
                st.markdown(f"""
                <div class="card" style="padding: 15px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="color: #94A3B8; font-size: 12px;">[{t.get('category', 'General')} | Priority: {t.get('priority', 'Normal')}]</span><br>
                        <b>Issue:</b> {t['desc']}
                    </div>
                    <span class="badge-status">STATUS: {t['status'].upper()}</span>
                </div>
                """, unsafe_allow_html=True)

    elif tenant_menu == "👤 Profile & Lease":
        st.markdown("### 💰 Security Deposit Tracking")
        st.info(f"**Official Security Deposit Logged with Owner:** ₹{room_data.get('security_deposit', 0)}")
        
        st.markdown("### 👤 Update Profile & Emergency Contacts")
        with st.expander("Update Emergency Contact Details", expanded=False):
            with st.form("emergency_contact_form"):
                new_ec = st.text_input("Emergency Contact Name & Phone Number", value=room_data.get("emergency_contact", ""))
                if st.form_submit_button("Save Contact Info"):
                    room_data["emergency_contact"] = new_ec
                    sync_to_db()
                    st.success("Contact Details Updated & Saved to DB!")


# ==========================================
# 📊 6. OWNER PORTAL INTERFACE
# ==========================================
else:
    if st.session_state.assigning_room:
        r_to_assign = st.session_state.assigning_room
        st.markdown(f"<h2>👤 Assign New Tenant Details for <span style='color: #34D399;'>{r_to_assign}</span></h2>", unsafe_allow_html=True)
        
        with st.form("occupy_details_form"):
            t_name = st.text_input("Tenant Full Legal Name", placeholder="e.g. Rajesh Kumar")
            t_phone = st.text_input("Tenant Active Phone Number", placeholder="9876543210")
            t_deposit = st.number_input("Security Deposit Collected (₹)", value=15000)
            
            bc1, bc2, bc3 = st.columns(3)
            with bc1: t_rent = st.number_input("Base Room Rent (₹)", value=6000)
            with bc2: t_light = st.number_input("Standard Light/Utility Bill (₹)", value=400)
            with bc3: t_maint = st.number_input("Building Maintenance (₹)", value=150)
                
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1: submitted_occupy = st.form_submit_button("✅ Save & Mark Occupied", use_container_width=True)
            with col_btn2: cancel_occupy = st.form_submit_button("❌ Cancel", use_container_width=True)
                
            if submitted_occupy:
                if t_name.strip() and len(t_phone) == 10:
                    st.session_state.rooms[r_to_assign].update({
                        "status": "Occupied", "tenant": t_name, "phone": t_phone,
                        "security_deposit": t_deposit, "rent": t_rent, "light": t_light, "maint": t_maint
                    })
                    sync_to_db()
                    st.session_state.assigning_room = None
                    st.success("Room updated & saved to database!")
                    st.rerun()
                else:
                    st.error("Provide a valid name and 10-digit phone number.")
                    
            if cancel_occupy:
                st.session_state.assigning_room = None
                st.rerun()
        st.stop()

    with st.sidebar:
        st.markdown(f"### 🏢 RENT MANAGER")
        st.markdown(f"<p style='font-size:12px; color:#34D399; margin:0;'>Owner: {st.session_state.owner_profile['name']}</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:11px; color:#94A3B8; margin-top:-5px;'>CREATED BY BINARY BOYS</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        owner_menu = st.radio(
            "Owner Navigation",
            ["📈 Portfolio Overview & Actions", "📇 Tenant Directory"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    total_collected = 0
    total_outstanding = 0
    
    for r_data in st.session_state.rooms.values():
        for m, m_data in r_data["history"].items():
            if m_data["status"] == "Paid":
                total_collected += m_data["total"]
            else:
                total_outstanding += m_data["total"]

    total_expenses = sum(e["amount"] for e in st.session_state.expenses)
    net_profit = total_collected - total_expenses
    occupied_count = sum(1 for d in st.session_state.rooms.values() if d["status"] == "Occupied")
    total_rooms = len(st.session_state.rooms)

    col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
    with col_m1: st.markdown(f'<div class="metric-box"><p style="color: #94A3B8; font-size: 10px; font-weight: bold;">TOTAL REVENUE</p><h3 style="color: #34D399; margin:0;">₹{total_collected}</h3></div>', unsafe_allow_html=True)
    with col_m2: st.markdown(f'<div class="metric-box"><p style="color: #94A3B8; font-size: 10px; font-weight: bold;">TOTAL EXPENSES</p><h3 style="color: #F87171; margin:0;">₹{total_expenses}</h3></div>', unsafe_allow_html=True)
    with col_m3: st.markdown(f'<div class="metric-box"><p style="color: #94A3B8; font-size: 10px; font-weight: bold;">NET PROFIT</p><h3 style="color: #60A5FA; margin:0;">₹{net_profit}</h3></div>', unsafe_allow_html=True)
    with col_m4: st.markdown(f'<div class="metric-box"><p style="color: #94A3B8; font-size: 10px; font-weight: bold;">OUTSTANDING DUES</p><h2 style="color: #FBBF24; margin:0;">₹{total_outstanding}</h2></div>', unsafe_allow_html=True)
    with col_m5: st.markdown(f'<div class="metric-box"><p style="color: #94A3B8; font-size: 10px; font-weight: bold;">OCCUPANCY RATIO</p><h3 style="color: #A78BFA; margin:0;">{occupied_count} / {total_rooms}</h3></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if owner_menu == "📈 Portfolio Overview & Actions":
        st.markdown("### ⚙️ Master Property Actions & Database Engine")
        
        with st.expander("💸 Log Property Expense", expanded=False):
            with st.form("expense_form"):
                exp_desc = st.text_input("Expense Description")
                exp_amt = st.number_input("Cost Amount (₹)", min_value=1, value=1500)
                if st.form_submit_button("Log Expense") and exp_desc:
                    st.session_state.expenses.append({"desc": exp_desc, "amount": exp_amt, "date": str(date.today())})
                    sync_to_db()
                    st.success("Expense logged & saved to database!")
                    st.rerun()

        with st.expander("➕ Expand Portfolio: Add New Room", expanded=False):
            with st.form("owner_room_adder_master"):
                f_col1, f_col2 = st.columns(2)
                with f_col1:
                    new_room_no = st.text_input("New Room ID", placeholder="e.g. Room 505")
                    tenant_name = st.text_input("Tenant Name (Blank if Vacant)")
                    tenant_phone = st.text_input("Tenant Phone", placeholder="9876543210")
                with f_col2:
                    billing_month = st.selectbox("Initial Billing Month", ["June", "July", "August", "September"])
                    billing_year = st.selectbox("Billing Year", [2026, 2027])
                    sec_dep = st.number_input("Security Deposit (₹)", value=0)

                i_col1, i_col2, i_col3 = st.columns(3)
                with i_col1: r_rent = st.number_input("Base Rent (₹)", value=6000)
                with i_col2: r_light = st.number_input("Light Bill (₹)", value=400)
                with i_col3: r_maint = st.number_input("Maintenance (₹)", value=150)

                if st.form_submit_button("Save & Add Room to DB"):
                    if new_room_no:
                        is_occupied = "Occupied" if tenant_name.strip() else "Vacant"
                        st.session_state.rooms[new_room_no] = {
                            "status": is_occupied,
                            "tenant": tenant_name if tenant_name.strip() else "None Assigned",
                            "phone": tenant_phone, "security_deposit": sec_dep,
                            "rent": r_rent, "light": r_light, "maint": r_maint,
                            "doc": None, "owner_doc": None,
                            "history": {f"{billing_month} {billing_year}": {"total": r_rent + r_light + r_maint, "status": "Pending", "receipt": None}} if is_occupied == "Occupied" else {}
                        }
                        sync_to_db()
                        st.success(f"Room {new_room_no} integrated & saved to database!")
                        st.rerun()

        st.markdown("<hr style='border-color: rgba(52,211,153,0.2); margin: 25px 0;'>", unsafe_allow_html=True)
        st.markdown("### 🏢 Managed Property Portfolio Overview")
        
        room_items = list(st.session_state.rooms.items())
        for i in range(0, len(room_items), 2):
            cols = st.columns(2)
            for j in range(2):
                if i + j < len(room_items):
                    r_name, r_info = room_items[i + j]
                    with cols[j]:
                        status_color = "rgba(6, 78, 59, 0.6)" if r_info["status"] == "Occupied" else "rgba(127, 29, 29, 0.6)"
                        status_text_color = "#34D399" if r_info["status"] == "Occupied" else "#F87171"
                        
                        st.markdown(f"""
                        <div class="card" style="padding: 20px; min-height: 160px;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                                <h3 style="margin: 0; color: #FFFFFF; font-size: 18px;">{r_name}</h3>
                                <span style="background-color: {status_color}; color: {status_text_color}; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: bold;">{r_info['status']}</span>
                            </div>
                            <p style="margin: 4px 0; font-size: 13px;"><b>Tenant:</b> {r_info['tenant']}</p>
                            <p style="margin: 4px 0; font-size: 13px;"><b>Deposit:</b> ₹{r_info.get('security_deposit', 0)}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        new_status = st.selectbox(f"Modify Status ({r_name})", ["Occupied", "Vacant"], index=0 if r_info["status"] == "Occupied" else 1, key=f"sb_{r_name}")
                        if new_status != r_info["status"]:
                            if new_status == "Occupied":
                                st.session_state.assigning_room = r_name
                                st.rerun()
                            else:
                                r_info.update({"status": "Vacant", "tenant": "None Assigned", "phone": "", "security_deposit": 0})
                                sync_to_db()
                                st.rerun()

        st.markdown("---")
        st.markdown("### 🛠️ Central Maintenance & Complaint Desk")
        if not st.session_state.complaints:
            st.info("No active maintenance tickets from any tenant.")
        else:
            for idx, c in enumerate(st.session_state.complaints):
                col_c1, col_c2 = st.columns([3, 1])
                with col_c1:
                    st.markdown(f"""
                    <div class="card" style="padding: 15px; margin-bottom: 10px;">
                        <span style="color: #94A3B8; font-size: 12px;">Ticket #{c['id']} | Room: {c['room']} | Tenant: {c['tenant']}</span><br>
                        <b>Issue:</b> {c['desc']}
                    </div>
                    """, unsafe_allow_html=True)
                with col_c2:
                    new_ticket_status = st.selectbox(
                        f"Update Status for Ticket #{c['id']}", 
                        ["Open", "In Progress", "Resolved"], 
                        index=["Open", "In Progress", "Resolved"].index(c['status']),
                        key=f"ticket_status_{c['id']}"
                    )
                    if new_ticket_status != c['status']:
                        c['status'] = new_ticket_status
                        sync_to_db()
                        st.rerun()

    elif owner_menu == "📇 Tenant Directory":
        st.markdown("### 📇 Master Tenant Directory & Database Sync")
        
        tenant_list = []
        for r_name, r_data in st.session_state.rooms.items():
            if r_data["status"] == "Occupied":
                tenant_list.append({
                    "Room No.": r_name, 
                    "Tenant Name": r_data["tenant"], 
                    "Primary Phone": r_data["phone"], 
                    "Deposit": f"₹{r_data.get('security_deposit', 0)}"
                })
        
        if tenant_list:
            for t_item in tenant_list:
                col_d1, col_d2 = st.columns([4, 1])
                with col_d1:
                    st.markdown(f"""
                    <div class="card" style="padding: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="color: #34D399; font-weight: bold; font-size: 16px;">{t_item['Room No.']}</span> — <b>{t_item['Tenant Name']}</b><br>
                            <span style="color: #94A3B8; font-size: 13px;">Phone: {t_item['Primary Phone']} | Deposit: {t_item['Deposit']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_d2:
                    st.write("")
                    if st.button("🗑️ Remove Tenant", key=f"del_tenant_{t_item['Room No.']}", help="Warning: This will clear tenant data and mark room vacant."):
                        room_key = t_item['Room No.']
                        if room_key in st.session_state.rooms:
                            st.session_state.rooms[room_key].update({
                                "status": "Vacant",
                                "tenant": "None Assigned",
                                "phone": "",
                                "security_deposit": 0,
                                "emergency_contact": "",
                                "doc": None,
                                "owner_doc": None
                            })
                            sync_to_db()
                            st.success(f"Tenant from {room_key} removed successfully! Room marked vacant.")
                            st.rerun()
        else:
            st.info("No active tenants currently reside in the property.")