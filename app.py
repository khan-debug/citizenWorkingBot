from flask import Flask, jsonify, request, render_template, redirect, url_for
from multi_agents import AgentOrchestrator
import json

# Initialize the Flask application
app = Flask(__name__)

# Initialize the multi-agent system
orchestrator = AgentOrchestrator()

# --- Hardcoded Policy Rules ---
# In a real application, this data would come from a database.
# For now, we are keeping it simple.
POLICY_RULES = {
    "education_schemes": [
        {
            "scheme_name": "Ehsaas Education Grant",
            "min_children": 2,
            "max_monthly_income": 30000,
            "description": "Provides a stipend for families with school-aged children.",
            "benefits": "Monthly stipend of PKR 2,000 per child, school supplies, uniform allowance",
            "required_documents": ["CNIC", "Children's birth certificates", "School enrollment proof", "Income certificate", "Bank account details"],
            "application_process": "Online application through Ehsaas portal or visit local Ehsaas center",
            "helpline": "0800-26477",
            "website": "https://ehsaas.gov.pk"
        },
        {
            "scheme_name": "Prime Minister's Education Initiative",
            "min_children": 1,
            "max_monthly_income": 40000,
            "description": "Supports education expenses for eligible families.",
            "benefits": "Educational stipend, laptop/tablet for students, scholarship opportunities",
            "required_documents": ["CNIC", "Student ID", "Academic records", "Income certificate", "Family registration certificate"],
            "application_process": "Apply through PM Education Portal or district education office",
            "helpline": "0800-12345",
            "website": "https://pm-education.gov.pk"
        },
        {
            "scheme_name": "Benazir Income Support Programme (BISP)",
            "min_children": 1,
            "max_monthly_income": 25000,
            "description": "Cash transfer program for poor families.",
            "benefits": "Monthly cash transfer of PKR 2,000, health insurance, education stipend",
            "required_documents": ["CNIC", "Family registration certificate", "Income certificate", "Bank account details", "Children's birth certificates"],
            "application_process": "Registration at BISP center or online through BISP portal",
            "helpline": "0800-26477",
            "website": "https://bisp.gov.pk"
        }
    ],
    "housing_schemes": [
        {
            "scheme_name": "Naya Pakistan Housing Scheme",
            "min_monthly_income": 25000,
            "max_monthly_income": 60000,
            "credit_check_required": True,
            "description": "Provides low-cost housing loans for eligible families.",
            "benefits": "Low-interest housing loan up to PKR 2.5 million, flexible payment terms",
            "required_documents": ["CNIC", "Income certificate", "Bank statements", "Employment letter", "Credit report", "Property documents"],
            "application_process": "Apply through Naya Pakistan Housing Portal or visit designated banks",
            "helpline": "0800-12345",
            "website": "https://nphda.gov.pk"
        },
        {
            "scheme_name": "Apna Ghar Scheme",
            "min_monthly_income": 20000,
            "max_monthly_income": 50000,
            "description": "Affordable housing for low-income families.",
            "benefits": "Subsidized housing units, low down payment, government guarantee",
            "required_documents": ["CNIC", "Income certificate", "Family registration certificate", "Bank account details", "Employment proof"],
            "application_process": "Apply through Apna Ghar portal or visit local housing authority",
            "helpline": "0800-98765",
            "website": "https://apnaghar.gov.pk"
        }
    ],
    "healthcare_schemes": [
        {
            "scheme_name": "Sehat Card Plus",
            "income_limit": 50000,
            "description": "Free healthcare coverage for eligible families.",
            "benefits": "Free treatment at government hospitals, emergency care, specialist consultations",
            "required_documents": ["CNIC", "Family registration certificate", "Income certificate", "Recent photograph"],
            "application_process": "Apply at Sehat Card centers or through online portal",
            "helpline": "0800-12345",
            "website": "https://sehatcard.gov.pk"
        },
        {
            "scheme_name": "Ehsaas Health Insurance",
            "income_limit": 30000,
            "description": "Health insurance for poor families.",
            "benefits": "Health insurance coverage, cashless treatment, medicine allowance",
            "required_documents": ["CNIC", "Income certificate", "Family registration certificate", "Bank account details"],
            "application_process": "Apply through Ehsaas portal or visit Ehsaas center",
            "helpline": "0800-26477",
            "website": "https://ehsaas.gov.pk"
        }
    ],
    "employment_schemes": [
        {
            "scheme_name": "Ehsaas Emergency Cash",
            "income_limit": 20000,
            "description": "Emergency financial assistance.",
            "benefits": "One-time cash assistance of PKR 12,000, immediate relief",
            "required_documents": ["CNIC", "Income certificate", "Emergency situation proof", "Bank account details"],
            "application_process": "Apply through Ehsaas emergency portal or SMS service",
            "helpline": "0800-26477",
            "website": "https://ehsaas.gov.pk"
        },
        {
            "scheme_name": "Kamyab Jawan Program",
            "age_limit": 35,
            "description": "Youth entrepreneurship and skill development.",
            "benefits": "Business loans up to PKR 5 million, skill training, mentorship",
            "required_documents": ["CNIC", "Educational certificates", "Business plan", "Bank account details", "Character certificate"],
            "application_process": "Apply through Kamyab Jawan portal or visit youth centers",
            "helpline": "0800-12345",
            "website": "https://kamyabjawan.gov.pk"
        }
    ]
}
# -----------------------------


@app.route("/")
def home():
    """Main page with issue submission form."""
    return render_template("index.html")


@app.route("/submit-issue", methods=["POST"])
def submit_issue():
    """Handle user issue submission and process through multi-agent system."""
    try:
        data = request.get_json()
        user_issue = data.get("issue", "")
        user_info = data.get("user_info", {})
        
        if not user_issue.strip():
            return jsonify({
                "status": "error",
                "message": "Please describe your issue"
            }), 400
        
        # Process through multi-agent system
        result = orchestrator.solve_user_issue(user_issue, user_info)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }), 500


@app.route("/api/eligibility-rules", methods=['GET'])
def get_eligibility_rules():
    """This endpoint returns all the current policy rules."""
    return jsonify(POLICY_RULES)


@app.route("/api/schemes", methods=['GET'])
def get_schemes():
    """Get all available schemes organized by category."""
    return jsonify(POLICY_RULES)


@app.route("/help")
def help_page():
    """Help page with instructions."""
    return render_template("help.html")


@app.route("/about")
def about_page():
    """About page."""
    return render_template("about.html")


@app.route("/api/scheme-details/<scheme_name>", methods=['GET'])
def get_scheme_details(scheme_name):
    """Get detailed information about a specific scheme."""
    try:
        # Find scheme in POLICY_RULES
        scheme_details = None
        for category, schemes in POLICY_RULES.items():
            for scheme in schemes:
                if scheme.get("scheme_name") == scheme_name:
                    scheme_details = {
                        "name": scheme.get("scheme_name"),
                        "description": scheme.get("description"),
                        "benefits": scheme.get("benefits", ""),
                        "application_process": scheme.get("application_process", ""),
                        "helpline": scheme.get("helpline", ""),
                        "website": scheme.get("website", ""),
                        "required_documents": scheme.get("required_documents", []),
                        "category": category.replace("_schemes", "").title()
                    }
                    break
            if scheme_details:
                break
        
        if scheme_details:
            return jsonify({
                "status": "success",
                "scheme": scheme_details
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Scheme not found"
            }), 404
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }), 500


@app.route("/api/collect-documents", methods=['POST'])
def collect_documents():
    """Collect required documents for a scheme."""
    try:
        data = request.get_json()
        scheme_name = data.get("scheme_name", "")
        user_info = data.get("user_info", {})
        
        if not scheme_name.strip():
            return jsonify({
                "status": "error",
                "message": "Scheme name is required"
            }), 400
        
        # Use DocumentCollectionAgent
        result = orchestrator.document_agent.collect_documents(scheme_name, user_info)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }), 500


@app.route("/api/helpline-info", methods=['POST'])
def get_helpline_info():
    """Get helpline information for a scheme or issue type."""
    try:
        data = request.get_json()
        scheme_name = data.get("scheme_name")
        issue_type = data.get("issue_type")
        
        # Use HelplineAgent
        result = orchestrator.helpline_agent.get_helpline_info(scheme_name, issue_type)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }), 500


@app.route("/api/forward-query", methods=['POST'])
def forward_query():
    """Forward user query to relevant department."""
    try:
        data = request.get_json()
        user_issue = data.get("issue", "")
        user_info = data.get("user_info", {})
        department = data.get("department")
        
        if not user_issue.strip():
            return jsonify({
                "status": "error",
                "message": "Issue description is required"
            }), 400
        
        # Use HelplineAgent
        result = orchestrator.helpline_agent.forward_query(user_issue, user_info, department)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }), 500


@app.route("/api/assist-application", methods=['POST'])
def assist_application():
    """Assist user with scheme application process."""
    try:
        data = request.get_json()
        scheme_name = data.get("scheme_name", "")
        user_info = data.get("user_info", {})
        documents = data.get("documents", {})
        
        if not scheme_name.strip():
            return jsonify({
                "status": "error",
                "message": "Scheme name is required"
            }), 400
        
        # Use ApplicationAssistantAgent
        result = orchestrator.application_agent.assist_application(scheme_name, user_info, documents)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }), 500


if __name__ == '__main__':
    # Runs the app on a local development server.
    # The port can be any number, 5000 is common for Flask.
    app.run(debug=True, port=5000)