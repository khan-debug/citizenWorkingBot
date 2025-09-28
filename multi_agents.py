"""
Multi-Agent System for Citizen Bot Pakistan
This module contains specialized AI agents that work together to help citizens.
"""

import os
import json
from typing import Dict, List, Any

# Try to import vertexai, fallback if not available
try:
    import vertexai
    from vertexai.generative_models import GenerativeModel
    VERTEXAI_AVAILABLE = True
except ImportError:
    print("⚠️  Vertex AI not available, using fallback mode")
    VERTEXAI_AVAILABLE = False
    vertexai = None
    GenerativeModel = None

# Set up authentication using service account key
if not os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service-account-key.json'

# Check if we're in fallback mode
FALLBACK_MODE = os.environ.get('FALLBACK_MODE', 'false').lower() == 'true' or not VERTEXAI_AVAILABLE

# Initialize Vertex AI with project ID and location (only if not in fallback mode)
if not FALLBACK_MODE and VERTEXAI_AVAILABLE:
    try:
        vertexai.init(project="ultimate-realm-473419-c7", location="us-central1")
    except Exception as e:
        print(f"⚠️  Warning: Could not initialize Vertex AI: {e}")
        print("🔄 Switching to fallback mode...")
        FALLBACK_MODE = True
        os.environ['FALLBACK_MODE'] = 'true'


class PolicyAgent:
    """Agent responsible for understanding government policies and schemes."""
    
    def __init__(self):
        if not FALLBACK_MODE and VERTEXAI_AVAILABLE and GenerativeModel:
            try:
                self.model = GenerativeModel("gemini-pro")
            except Exception as e:
                print(f"⚠️  Warning: Could not initialize Gemini model: {e}")
                self.model = None
        else:
            self.model = None
        self.policies = {
            "education_schemes": [
                {
                    "name": "Ehsaas Education Grant",
                    "min_children": 2,
                    "max_monthly_income": 30000,
                    "description": "Provides monthly stipend for families with school-aged children",
                    "benefits": "Monthly stipend of PKR 2,000 per child, school supplies, uniform allowance",
                    "required_documents": ["CNIC", "Children's birth certificates", "School enrollment proof", "Income certificate", "Bank account details"],
                    "application_process": "Online application through Ehsaas portal or visit local Ehsaas center",
                    "helpline": "0800-26477",
                    "website": "https://ehsaas.gov.pk"
                },
                {
                    "name": "Prime Minister's Education Initiative",
                    "min_children": 1,
                    "max_monthly_income": 40000,
                    "description": "Supports education expenses for eligible families",
                    "benefits": "Educational stipend, laptop/tablet for students, scholarship opportunities",
                    "required_documents": ["CNIC", "Student ID", "Academic records", "Income certificate", "Family registration certificate"],
                    "application_process": "Apply through PM Education Portal or district education office",
                    "helpline": "0800-12345",
                    "website": "https://pm-education.gov.pk"
                },
                {
                    "name": "Benazir Income Support Programme (BISP)",
                    "min_children": 1,
                    "max_monthly_income": 25000,
                    "description": "Cash transfer program for poor families",
                    "benefits": "Monthly cash transfer of PKR 2,000, health insurance, education stipend",
                    "required_documents": ["CNIC", "Family registration certificate", "Income certificate", "Bank account details", "Children's birth certificates"],
                    "application_process": "Registration at BISP center or online through BISP portal",
                    "helpline": "0800-26477",
                    "website": "https://bisp.gov.pk"
                }
            ],
            "housing_schemes": [
                {
                    "name": "Naya Pakistan Housing Scheme",
                    "min_monthly_income": 25000,
                    "max_monthly_income": 60000,
                    "credit_check_required": True,
                    "description": "Provides low-cost housing loans",
                    "benefits": "Low-interest housing loan up to PKR 2.5 million, flexible payment terms",
                    "required_documents": ["CNIC", "Income certificate", "Bank statements", "Employment letter", "Credit report", "Property documents"],
                    "application_process": "Apply through Naya Pakistan Housing Portal or visit designated banks",
                    "helpline": "0800-12345",
                    "website": "https://nphda.gov.pk"
                },
                {
                    "name": "Apna Ghar Scheme",
                    "min_monthly_income": 20000,
                    "max_monthly_income": 50000,
                    "description": "Affordable housing for low-income families",
                    "benefits": "Subsidized housing units, low down payment, government guarantee",
                    "required_documents": ["CNIC", "Income certificate", "Family registration certificate", "Bank account details", "Employment proof"],
                    "application_process": "Apply through Apna Ghar portal or visit local housing authority",
                    "helpline": "0800-98765",
                    "website": "https://apnaghar.gov.pk"
                }
            ],
            "healthcare_schemes": [
                {
                    "name": "Sehat Card Plus",
                    "income_limit": 50000,
                    "description": "Free healthcare coverage for eligible families",
                    "benefits": "Free treatment at government hospitals, emergency care, specialist consultations",
                    "required_documents": ["CNIC", "Family registration certificate", "Income certificate", "Recent photograph"],
                    "application_process": "Apply at Sehat Card centers or through online portal",
                    "helpline": "0800-12345",
                    "website": "https://sehatcard.gov.pk"
                },
                {
                    "name": "Ehsaas Health Insurance",
                    "income_limit": 30000,
                    "description": "Health insurance for poor families",
                    "benefits": "Health insurance coverage, cashless treatment, medicine allowance",
                    "required_documents": ["CNIC", "Income certificate", "Family registration certificate", "Bank account details"],
                    "application_process": "Apply through Ehsaas portal or visit Ehsaas center",
                    "helpline": "0800-26477",
                    "website": "https://ehsaas.gov.pk"
                }
            ],
            "employment_schemes": [
                {
                    "name": "Ehsaas Emergency Cash",
                    "income_limit": 20000,
                    "description": "Emergency financial assistance",
                    "benefits": "One-time cash assistance of PKR 12,000, immediate relief",
                    "required_documents": ["CNIC", "Income certificate", "Emergency situation proof", "Bank account details"],
                    "application_process": "Apply through Ehsaas emergency portal or SMS service",
                    "helpline": "0800-26477",
                    "website": "https://ehsaas.gov.pk"
                },
                {
                    "name": "Kamyab Jawan Program",
                    "age_limit": 35,
                    "description": "Youth entrepreneurship and skill development",
                    "benefits": "Business loans up to PKR 5 million, skill training, mentorship",
                    "required_documents": ["CNIC", "Educational certificates", "Business plan", "Bank account details", "Character certificate"],
                    "application_process": "Apply through Kamyab Jawan portal or visit youth centers",
                    "helpline": "0800-12345",
                    "website": "https://kamyabjawan.gov.pk"
                }
            ]
        }
    
    def analyze_user_issue(self, user_issue: str) -> Dict[str, Any]:
        """Analyze user issue and identify relevant policies."""
        if FALLBACK_MODE or self.model is None:
            return self._fallback_policy_analysis(user_issue)
        
        try:
            prompt = f"""
            You are a policy expert for Pakistan government schemes. Analyze this citizen's issue and identify:
            1. What type of help they need (education, housing, healthcare, etc.)
            2. Which specific schemes might be relevant
            3. Key information needed to determine eligibility
            
            Citizen's issue: "{user_issue}"
            
            Available schemes: {json.dumps(self.policies, indent=2)}
            
            Respond in JSON format with:
            {{
                "issue_type": "education/housing/healthcare/general",
                "relevant_schemes": ["scheme1", "scheme2"],
                "required_info": ["income", "family_size", "location"],
                "confidence": 0.8
            }}
            """
            
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            return result
        except Exception as e:
            print(f"⚠️  AI analysis failed: {e}")
            return self._fallback_policy_analysis(user_issue)
    
    def _fallback_policy_analysis(self, user_issue: str) -> Dict[str, Any]:
        """Fallback analysis using rule-based approach."""
        issue_lower = user_issue.lower()
        
        # More comprehensive keyword matching
        education_keywords = ["education", "school", "student", "study", "children", "kids", "tuition", "fees", "scholarship", "learning"]
        housing_keywords = ["house", "housing", "home", "property", "loan", "mortgage", "apartment", "residence", "accommodation"]
        healthcare_keywords = ["health", "medical", "hospital", "treatment", "doctor", "medicine", "illness", "surgery", "card", "insurance"]
        employment_keywords = ["job", "employment", "work", "income", "money", "cash", "salary", "business", "loan", "entrepreneur", "youth"]
        
        # Count keyword matches for better accuracy
        education_score = sum(1 for keyword in education_keywords if keyword in issue_lower)
        housing_score = sum(1 for keyword in housing_keywords if keyword in issue_lower)
        healthcare_score = sum(1 for keyword in healthcare_keywords if keyword in issue_lower)
        employment_score = sum(1 for keyword in employment_keywords if keyword in issue_lower)
        
        # Determine issue type based on highest score
        scores = {
            "education": education_score,
            "housing": housing_score,
            "healthcare": healthcare_score,
            "employment": employment_score
        }
        
        issue_type = max(scores, key=scores.get) if max(scores.values()) > 0 else "general"
        
        # Get relevant schemes based on issue type
        relevant_schemes = []
        required_info = []
        
        if issue_type == "education":
            relevant_schemes = [
                "Ehsaas Education Grant",
                "Prime Minister's Education Initiative", 
                "Benazir Income Support Programme (BISP)"
            ]
            required_info = ["monthly_income", "number_of_children", "children_ages", "location"]
            
        elif issue_type == "housing":
            relevant_schemes = [
                "Naya Pakistan Housing Scheme",
                "Apna Ghar Scheme"
            ]
            required_info = ["monthly_income", "credit_score", "employment_status", "location"]
            
        elif issue_type == "healthcare":
            relevant_schemes = [
                "Sehat Card Plus",
                "Ehsaas Health Insurance"
            ]
            required_info = ["monthly_income", "family_size", "medical_condition", "location"]
            
        elif issue_type == "employment":
            relevant_schemes = [
                "Ehsaas Emergency Cash",
                "Kamyab Jawan Program",
                "Benazir Income Support Programme (BISP)"
            ]
            required_info = ["monthly_income", "family_size", "employment_status", "age"]
            
        else:
            # General case - provide multiple options
            relevant_schemes = [
                "Ehsaas Education Grant",
                "Sehat Card Plus",
                "Ehsaas Emergency Cash",
                "Benazir Income Support Programme (BISP)"
            ]
            required_info = ["monthly_income", "family_size", "location", "specific_needs"]
        
        # Calculate confidence based on keyword matches
        confidence = min(0.9, 0.5 + (max(scores.values()) * 0.1))
        
        return {
            "issue_type": issue_type,
            "relevant_schemes": relevant_schemes,
            "required_info": required_info,
            "confidence": confidence,
            "analysis_details": {
                "keyword_matches": scores,
                "detected_needs": self._extract_specific_needs(issue_lower),
                "urgency_level": self._assess_urgency(issue_lower)
            }
        }
    
    def _extract_specific_needs(self, issue_lower: str) -> List[str]:
        """Extract specific needs from the user issue."""
        needs = []
        
        if any(word in issue_lower for word in ["urgent", "emergency", "immediate", "asap"]):
            needs.append("urgent_assistance")
        
        if any(word in issue_lower for word in ["financial", "money", "cash", "income"]):
            needs.append("financial_support")
        
        if any(word in issue_lower for word in ["family", "children", "kids"]):
            needs.append("family_support")
        
        if any(word in issue_lower for word in ["medical", "health", "treatment"]):
            needs.append("healthcare_support")
        
        if any(word in issue_lower for word in ["education", "school", "study"]):
            needs.append("education_support")
        
        return needs if needs else ["general_assistance"]
    
    def _assess_urgency(self, issue_lower: str) -> str:
        """Assess the urgency level of the issue."""
        urgent_keywords = ["urgent", "emergency", "immediate", "asap", "critical", "desperate"]
        moderate_keywords = ["soon", "quickly", "fast", "priority"]
        
        if any(keyword in issue_lower for keyword in urgent_keywords):
            return "high"
        elif any(keyword in issue_lower for keyword in moderate_keywords):
            return "medium"
        else:
            return "low"


class EligibilityAgent:
    """Agent responsible for determining eligibility for government schemes."""
    
    def __init__(self):
        if not FALLBACK_MODE and VERTEXAI_AVAILABLE and GenerativeModel:
            try:
                self.model = GenerativeModel("gemini-pro")
            except Exception as e:
                print(f"⚠️  Warning: Could not initialize Gemini model: {e}")
                self.model = None
        else:
            self.model = None
    
    def check_eligibility(self, scheme_name: str, user_info: Dict[str, Any]) -> Dict[str, Any]:
        """Check if user is eligible for a specific scheme."""
        if FALLBACK_MODE or self.model is None:
            return self._fallback_eligibility_check(scheme_name, user_info)
        
        try:
            prompt = f"""
            You are an eligibility expert for Pakistan government schemes. Determine if this citizen is eligible:
            
            Scheme: {scheme_name}
            User Information: {json.dumps(user_info, indent=2)}
            
            Respond in JSON format:
            {{
                "eligible": true/false,
                "reason": "explanation of eligibility decision",
                "missing_requirements": ["requirement1", "requirement2"],
                "next_steps": ["step1", "step2"]
            }}
            """
            
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            return result
        except Exception as e:
            print(f"⚠️  AI eligibility check failed: {e}")
            return self._fallback_eligibility_check(scheme_name, user_info)
    
    def _fallback_eligibility_check(self, scheme_name: str, user_info: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback eligibility check using rule-based approach."""
        monthly_income = user_info.get("monthly_income", 0)
        family_size = user_info.get("family_size", 0)
        number_of_children = user_info.get("number_of_children", 0)
        
        # Get scheme details from PolicyAgent
        policy_agent = PolicyAgent()
        scheme_details = self._find_scheme_details(scheme_name, policy_agent.policies)
        
        if not scheme_details:
                return {
                "eligible": False,
                "reason": "Scheme not found in our database",
                "missing_requirements": ["Valid scheme name required"],
                "next_steps": ["Contact helpline for assistance", "Check official government websites"]
            }
        
        # Check eligibility based on scheme type and criteria
        eligible = True
        missing_requirements = []
        reasons = []
        
        # Education schemes
        if "Education" in scheme_name or "Ehsaas Education Grant" in scheme_name:
            # Check income first
            if monthly_income > 0 and monthly_income > 30000:
                eligible = False
                missing_requirements.append(f"Income exceeds limit (your income: PKR {monthly_income:,}, max allowed: PKR 30,000)")
                reasons.append("Monthly income is too high for this scheme")
            elif monthly_income > 0 and monthly_income <= 30000:
                reasons.append(f"✅ Income is within limit (PKR {monthly_income:,} ≤ PKR 30,000)")
            
            # Check children requirement
            if number_of_children > 0 and number_of_children < 2:
                eligible = False
                missing_requirements.append(f"Need at least 2 school-aged children (you have: {number_of_children})")
                reasons.append("Family size requirement not met")
            elif number_of_children >= 2:
                reasons.append(f"✅ Family size requirement met ({number_of_children} children ≥ 2 required)")
            
            # If we have both income and children info, determine eligibility
            if monthly_income > 0 and number_of_children > 0:
                if monthly_income <= 30000 and number_of_children >= 2:
                    reasons.append("🎉 You are eligible for this education scheme!")
                    eligible = True
                else:
                    eligible = False
            elif monthly_income > 0 and number_of_children == 0:
                # Only income provided, be more lenient
                if monthly_income <= 30000:
                    reasons.append("✅ Income requirement met, but need at least 2 children")
                    eligible = False
                    missing_requirements.append("Need at least 2 school-aged children")
                else:
                    eligible = False
            elif monthly_income == 0 and number_of_children > 0:
                # Only children provided, be more lenient
                if number_of_children >= 2:
                    reasons.append("✅ Family size requirement met, but need income information")
                    eligible = False
                    missing_requirements.append("Income information required")
                else:
                    eligible = False
            else:
                # No specific info provided, be helpful
                reasons.append("ℹ️ Please provide income and family size for accurate assessment")
                eligible = False
                missing_requirements.append("Income and family size information required")
        
        elif "Prime Minister's Education Initiative" in scheme_name:
            # Check income first
            if monthly_income > 0 and monthly_income > 40000:
                eligible = False
                missing_requirements.append(f"Income exceeds limit (your income: PKR {monthly_income:,}, max allowed: PKR 40,000)")
                reasons.append("Monthly income is too high for this scheme")
            elif monthly_income > 0 and monthly_income <= 40000:
                reasons.append(f"✅ Income is within limit (PKR {monthly_income:,} ≤ PKR 40,000)")
            
            # Check children requirement
            if number_of_children > 0 and number_of_children < 1:
                eligible = False
                missing_requirements.append(f"Need at least 1 school-aged child (you have: {number_of_children})")
                reasons.append("Family size requirement not met")
            elif number_of_children >= 1:
                reasons.append(f"✅ Family size requirement met ({number_of_children} children ≥ 1 required)")
            
            # If we have both income and children info, determine eligibility
            if monthly_income > 0 and number_of_children > 0:
                if monthly_income <= 40000 and number_of_children >= 1:
                    reasons.append("🎉 You are eligible for this education initiative!")
                    eligible = True
                else:
                    eligible = False
            elif monthly_income > 0 and number_of_children == 0:
                # Only income provided, be more lenient
                if monthly_income <= 40000:
                    reasons.append("✅ Income requirement met, but need at least 1 child")
                    eligible = False
                    missing_requirements.append("Need at least 1 school-aged child")
                else:
                    eligible = False
            elif monthly_income == 0 and number_of_children > 0:
                # Only children provided, be more lenient
                if number_of_children >= 1:
                    reasons.append("✅ Family size requirement met, but need income information")
                    eligible = False
                    missing_requirements.append("Income information required")
                else:
                    eligible = False
            else:
                # No specific info provided, be helpful
                reasons.append("ℹ️ Please provide income and family size for accurate assessment")
                eligible = False
                missing_requirements.append("Income and family size information required")
        
        elif "BISP" in scheme_name or "Benazir Income Support Programme" in scheme_name:
            # Check income first
            if monthly_income > 0 and monthly_income > 25000:
                eligible = False
                missing_requirements.append(f"Income exceeds limit (your income: PKR {monthly_income:,}, max allowed: PKR 25,000)")
                reasons.append("Monthly income is too high for this scheme")
            elif monthly_income > 0 and monthly_income <= 25000:
                reasons.append(f"✅ Income is within limit (PKR {monthly_income:,} ≤ PKR 25,000)")
            
            # Check family size requirement
            if family_size > 0 and family_size < 2:
                eligible = False
                missing_requirements.append(f"Need at least 2 family members (you have: {family_size})")
                reasons.append("Family size requirement not met")
            elif family_size >= 2:
                reasons.append(f"✅ Family size requirement met ({family_size} family members ≥ 2 required)")
            
            # If we have both income and family info, determine eligibility
            if monthly_income > 0 and family_size > 0:
                if monthly_income <= 25000 and family_size >= 2:
                    reasons.append("🎉 You are eligible for BISP support!")
                    eligible = True
                else:
                    eligible = False
            elif monthly_income > 0 and family_size == 0:
                # Only income provided, be more lenient
                if monthly_income <= 25000:
                    reasons.append("✅ Income requirement met, but need at least 2 family members")
                    eligible = False
                    missing_requirements.append("Need at least 2 family members")
                else:
                    eligible = False
            elif monthly_income == 0 and family_size > 0:
                # Only family size provided, be more lenient
                if family_size >= 2:
                    reasons.append("✅ Family size requirement met, but need income information")
                    eligible = False
                    missing_requirements.append("Income information required")
                else:
                    eligible = False
            else:
                # No specific info provided, be helpful
                reasons.append("ℹ️ Please provide income and family size for accurate assessment")
                eligible = False
                missing_requirements.append("Income and family size information required")
        
        # Housing schemes
        elif "Housing" in scheme_name or "Naya Pakistan Housing" in scheme_name:
            # Check income range
            if monthly_income > 0 and monthly_income < 25000:
                eligible = False
                missing_requirements.append(f"Income too low (your income: PKR {monthly_income:,}, minimum required: PKR 25,000)")
                reasons.append("Income too low for housing loan")
            elif monthly_income > 0 and monthly_income > 60000:
                eligible = False
                missing_requirements.append(f"Income exceeds limit (your income: PKR {monthly_income:,}, max allowed: PKR 60,000)")
                reasons.append("Income too high for this scheme")
            elif monthly_income > 0:
                reasons.append(f"✅ Income is within range (PKR {monthly_income:,} is between PKR 25,000 - PKR 60,000)")
                eligible = True
            
            if eligible and monthly_income > 0:
                reasons.append("🎉 You are eligible for housing loan!")
            elif monthly_income == 0:
                reasons.append("ℹ️ Please provide income information for accurate assessment")
                eligible = False
                missing_requirements.append("Income information required")
        
        elif "Apna Ghar" in scheme_name:
            # Check income range
            if monthly_income > 0 and monthly_income < 20000:
                eligible = False
                missing_requirements.append(f"Income too low (your income: PKR {monthly_income:,}, minimum required: PKR 20,000)")
                reasons.append("Income too low for this scheme")
            elif monthly_income > 0 and monthly_income > 50000:
                eligible = False
                missing_requirements.append(f"Income exceeds limit (your income: PKR {monthly_income:,}, max allowed: PKR 50,000)")
                reasons.append("Income too high for this scheme")
            elif monthly_income > 0:
                reasons.append(f"✅ Income is within range (PKR {monthly_income:,} is between PKR 20,000 - PKR 50,000)")
                eligible = True
            
            if eligible and monthly_income > 0:
                reasons.append("🎉 You are eligible for Apna Ghar scheme!")
            elif monthly_income == 0:
                reasons.append("ℹ️ Please provide income information for accurate assessment")
                eligible = False
                missing_requirements.append("Income information required")
        
        # Healthcare schemes
        elif "Sehat Card" in scheme_name:
            # Check income limit
            if monthly_income > 0 and monthly_income > 50000:
                eligible = False
                missing_requirements.append(f"Income exceeds limit (your income: PKR {monthly_income:,}, max allowed: PKR 50,000)")
                reasons.append("Income too high for free healthcare")
            elif monthly_income > 0:
                reasons.append(f"✅ Income is within limit (PKR {monthly_income:,} ≤ PKR 50,000)")
                eligible = True
            
            if eligible and monthly_income > 0:
                reasons.append("🎉 You are eligible for Sehat Card!")
            elif monthly_income == 0:
                reasons.append("ℹ️ Please provide income information for accurate assessment")
                eligible = False
                missing_requirements.append("Income information required")
        
        elif "Ehsaas Health Insurance" in scheme_name:
            # Check income limit
            if monthly_income > 0 and monthly_income > 30000:
                eligible = False
                missing_requirements.append(f"Income exceeds limit (your income: PKR {monthly_income:,}, max allowed: PKR 30,000)")
                reasons.append("Income too high for health insurance")
            elif monthly_income > 0:
                reasons.append(f"✅ Income is within limit (PKR {monthly_income:,} ≤ PKR 30,000)")
                eligible = True
            
            if eligible and monthly_income > 0:
                reasons.append("🎉 You are eligible for Ehsaas Health Insurance!")
            elif monthly_income == 0:
                reasons.append("ℹ️ Please provide income information for accurate assessment")
                eligible = False
                missing_requirements.append("Income information required")
        
        # Employment schemes
        elif "Emergency Cash" in scheme_name:
            # Check income limit
            if monthly_income > 0 and monthly_income > 20000:
                eligible = False
                missing_requirements.append(f"Income exceeds limit (your income: PKR {monthly_income:,}, max allowed: PKR 20,000)")
                reasons.append("Income too high for emergency assistance")
            elif monthly_income > 0:
                reasons.append(f"✅ Income is within limit (PKR {monthly_income:,} ≤ PKR 20,000)")
                eligible = True
            
            if eligible and monthly_income > 0:
                reasons.append("🎉 You are eligible for Emergency Cash assistance!")
            elif monthly_income == 0:
                reasons.append("ℹ️ Please provide income information for accurate assessment")
                eligible = False
                missing_requirements.append("Income information required")
        
        elif "Kamyab Jawan" in scheme_name:
            age = user_info.get("age", 0)
            # Check age requirement
            if age > 0 and age > 35:
                eligible = False
                missing_requirements.append(f"Age exceeds limit (your age: {age} years, max allowed: 35 years)")
                reasons.append("Age requirement not met")
            elif age > 0 and age < 18:
                eligible = False
                missing_requirements.append(f"Minimum age required (your age: {age} years, minimum required: 18 years)")
                reasons.append("Age requirement not met")
            elif age > 0:
                reasons.append(f"✅ Age requirement met ({age} years is between 18-35)")
                eligible = True
            
            if eligible and age > 0:
                reasons.append("🎉 You are eligible for Kamyab Jawan program!")
            elif age == 0:
                reasons.append("ℹ️ Please provide age information for accurate assessment")
                eligible = False
                missing_requirements.append("Age information required")
        
        # Default case - be more helpful and lenient
        else:
            if monthly_income == 0:
                missing_requirements.append("Income information required for accurate assessment")
                reasons.append("Need income information to determine eligibility")
                eligible = False
            else:
                reasons.append(f"✅ Basic eligibility criteria appear to be met (income: PKR {monthly_income:,})")
                eligible = True
                reasons.append("ℹ️ This scheme may be suitable for you. Contact helpline for detailed assessment.")
        
        # Generate next steps
        next_steps = []
        if eligible:
            next_steps = [
                "🎯 Apply online through official website",
                "📋 Gather all required documents",
                "📞 Contact helpline for guidance",
                "🏛️ Visit local office for assistance"
            ]
        else:
            next_steps = [
                "🔍 Check other available schemes that might be suitable",
                "📞 Contact helpline for alternative options",
                "🏛️ Visit local government office for personalized assistance",
                "💡 Consider ways to improve eligibility criteria"
            ]
        
        return {
            "eligible": eligible,
            "reason": "; ".join(reasons) if reasons else "Eligibility determined based on provided information",
            "missing_requirements": missing_requirements,
            "next_steps": next_steps
        }
    
    def _find_scheme_details(self, scheme_name: str, policies: Dict) -> Dict:
        """Find scheme details from policies."""
        for category, schemes in policies.items():
            for scheme in schemes:
                if scheme["name"] == scheme_name:
                    return scheme
        return None


class ExplanationAgent:
    """Agent responsible for explaining complex information in simple terms."""
    
    def __init__(self):
        if not FALLBACK_MODE and VERTEXAI_AVAILABLE and GenerativeModel:
            try:
                self.model = GenerativeModel("gemini-pro")
            except Exception as e:
                print(f"⚠️  Warning: Could not initialize Gemini model: {e}")
                self.model = None
        else:
            self.model = None
    
    def explain_in_plain_language(self, analysis_data: Dict[str, Any]) -> str:
        """Convert analysis data to simple, citizen-friendly language."""
        try:
            # Extract key information from analysis
            issue_analysis = analysis_data.get("issue_analysis", {})
            issue_type = issue_analysis.get("issue_type", "general")
            relevant_schemes = issue_analysis.get("relevant_schemes", [])
            analysis_details = issue_analysis.get("analysis_details", {})
            urgency_level = analysis_details.get("urgency_level", "low")
            detected_needs = analysis_details.get("detected_needs", [])
            
            eligibility_results = analysis_data.get("eligibility_results", [])
            user_info = analysis_data.get("user_info", {})
            
            # Create a structured explanation
            explanation_parts = []
            
            # Personalized greeting based on urgency
            if urgency_level == "high":
                explanation_parts.append("🚨 Assalam-o-Alaikum! Main aapki urgent madad kar raha hun.")
            else:
                explanation_parts.append("Assalam-o-Alaikum! Main aapki madad kar raha hun.")
            explanation_parts.append("")
            
            # Issue analysis with more detail
            if issue_type != "general":
                explanation_parts.append(f"📋 Aapka issue {issue_type} category mein aata hai.")
                
                # Add specific needs detected
                if detected_needs:
                    explanation_parts.append("Main ne ye specific needs detect ki hain:")
                    for need in detected_needs:
                        if need == "urgent_assistance":
                            explanation_parts.append("   🚨 Urgent assistance required")
                        elif need == "financial_support":
                            explanation_parts.append("   💰 Financial support needed")
                        elif need == "family_support":
                            explanation_parts.append("   👨‍👩‍👧‍👦 Family support required")
                        elif need == "healthcare_support":
                            explanation_parts.append("   🏥 Healthcare support needed")
                        elif need == "education_support":
                            explanation_parts.append("   📚 Education support required")
            else:
                explanation_parts.append("📋 Main aapke issue ko samjha hun aur aapke liye best options dhund raha hun.")
            
            explanation_parts.append("")
            
            # Scheme recommendations with better formatting
            if relevant_schemes:
                explanation_parts.append("🎯 Aapke liye ye schemes suitable hain:")
                for i, scheme in enumerate(relevant_schemes, 1):
                    explanation_parts.append(f"   {i}. {scheme}")
                explanation_parts.append("")
            
            # Eligibility results with improved formatting
            if eligibility_results:
                eligible_count = sum(1 for result in eligibility_results if result.get("eligibility", {}).get("eligible", False))
                total_count = len(eligibility_results)
                
                explanation_parts.append(f"✅ Eligibility Check Results ({eligible_count}/{total_count} eligible):")
                explanation_parts.append("")
                
                for result in eligibility_results:
                    scheme_name = result.get("scheme", "")
                    eligibility = result.get("eligibility", {})
                    is_eligible = eligibility.get("eligible", False)
                    reason = eligibility.get("reason", "")
                    next_steps = eligibility.get("next_steps", [])
                    
                    if is_eligible:
                        explanation_parts.append(f"   ✅ {scheme_name}: Aap ELIGIBLE hain!")
                        explanation_parts.append(f"      📝 Reason: {reason}")
                        if next_steps:
                            explanation_parts.append("      🎯 Next Steps:")
                            for step in next_steps[:3]:  # Show only first 3 steps
                                explanation_parts.append(f"        • {step}")
                    else:
                        explanation_parts.append(f"   ❌ {scheme_name}: Currently not eligible")
                        explanation_parts.append(f"      📝 Reason: {reason}")
                        missing_reqs = eligibility.get("missing_requirements", [])
                        if missing_reqs:
                            explanation_parts.append("      ⚠️ Missing Requirements:")
                            for req in missing_reqs[:2]:  # Show only first 2 missing requirements
                                explanation_parts.append(f"        • {req}")
                        if next_steps:
                            explanation_parts.append("      💡 Suggestions:")
                            for step in next_steps[:2]:  # Show only first 2 suggestions
                                explanation_parts.append(f"        • {step}")
                explanation_parts.append("")
            
            # Personalized financial analysis
            monthly_income = user_info.get("monthly_income", 0)
            family_size = user_info.get("family_size", 0)
            location = user_info.get("location", "")
            
            if monthly_income > 0:
                explanation_parts.append("💰 Aapki Financial Analysis:")
                if monthly_income <= 20000:
                    explanation_parts.append("   🟢 Low income - Multiple schemes available")
                    explanation_parts.append("   💡 Priority: Emergency cash, BISP, Health cards")
                elif monthly_income <= 30000:
                    explanation_parts.append("   🟡 Moderate income - Several schemes available")
                    explanation_parts.append("   💡 Priority: Education grants, Health insurance")
                elif monthly_income <= 50000:
                    explanation_parts.append("   🟠 Higher income - Limited schemes available")
                    explanation_parts.append("   💡 Priority: Housing loans, Education initiatives")
                else:
                    explanation_parts.append("   🔴 High income - Very limited schemes")
                    explanation_parts.append("   💡 Priority: Housing schemes, Business loans")
                explanation_parts.append("")
            
            # Location-specific advice
            if location:
                explanation_parts.append(f"📍 Location: {location}")
                explanation_parts.append("   🏛️ Visit your local government office")
                explanation_parts.append("   📞 Contact local helpline numbers")
                explanation_parts.append("")
            
            # Action-oriented guidance
            explanation_parts.append("🚀 Immediate Action Steps:")
            explanation_parts.append("   1. 📋 Gather required documents")
            explanation_parts.append("   2. 🌐 Visit official websites")
            explanation_parts.append("   3. 📞 Call helpline numbers")
            explanation_parts.append("   4. 🏛️ Visit local government office")
            explanation_parts.append("")
            
            # Encouraging closing
            if eligible_count > 0:
                explanation_parts.append("🎉 Good news! Aap eligible hain for some schemes!")
                explanation_parts.append("📞 Contact helpline for detailed guidance.")
            else:
                explanation_parts.append("💪 Don't worry! Other options available.")
                explanation_parts.append("📞 Contact helpline for alternative solutions.")
            
            explanation_parts.append("")
            explanation_parts.append("🤲 Allah aapki madad kare! (May Allah help you!)")
            
            return "\n".join(explanation_parts)
            
        except Exception as e:
            return self._fallback_explanation(analysis_data)
    
    def _fallback_explanation(self, analysis_data: Dict[str, Any]) -> str:
        """Fallback explanation using rule-based approach."""
        try:
            # Extract key information from analysis
            issue_type = analysis_data.get("issue_analysis", {}).get("issue_type", "general")
            relevant_schemes = analysis_data.get("issue_analysis", {}).get("relevant_schemes", [])
            eligibility_results = analysis_data.get("eligibility_results", [])
            user_info = analysis_data.get("user_info", {})
            
            # Create a structured explanation
            explanation_parts = []
            
            # Greeting
            explanation_parts.append("Assalam-o-Alaikum! Main aapki madad kar raha hun. 🇵🇰")
            explanation_parts.append("")
            
            # Issue analysis
            if issue_type != "general":
                explanation_parts.append(f"📋 Aapka issue {issue_type} category mein aata hai.")
            else:
                explanation_parts.append("📋 Main aapke issue ko samjha hun.")
            
            explanation_parts.append("")
            
            # Scheme recommendations
            if relevant_schemes:
                explanation_parts.append("🎯 Aapke liye ye schemes suitable hain:")
                for scheme in relevant_schemes:
                    explanation_parts.append(f"   • {scheme}")
                explanation_parts.append("")
            
            # Eligibility results with detailed explanations
            if eligibility_results:
                explanation_parts.append("📊 Eligibility Check Results:")
                eligible_count = 0
                
                for result in eligibility_results:
                    scheme_name = result.get("scheme", "")
                    eligibility = result.get("eligibility", {})
                    is_eligible = eligibility.get("eligible", False)
                    reason = eligibility.get("reason", "")
                    next_steps = eligibility.get("next_steps", [])
                    
                    if is_eligible:
                        eligible_count += 1
                        explanation_parts.append(f"   ✅ [ELIGIBLE] {scheme_name}")
                        explanation_parts.append(f"      🎉 {reason}")
                        if next_steps:
                            explanation_parts.append("      📋 Next Steps:")
                            for step in next_steps:
                                explanation_parts.append(f"        • {step}")
                    else:
                        explanation_parts.append(f"   ❌ [NOT ELIGIBLE] {scheme_name}")
                        explanation_parts.append(f"      📝 {reason}")
                        missing_reqs = eligibility.get("missing_requirements", [])
                        if missing_reqs:
                            explanation_parts.append("      ⚠️ Missing Requirements:")
                            for req in missing_reqs:
                                explanation_parts.append(f"        • {req}")
                        if next_steps:
                            explanation_parts.append("      💡 Suggestions:")
                            for step in next_steps:
                                explanation_parts.append(f"        • {step}")
                explanation_parts.append("")
                
                # Summary
                if eligible_count > 0:
                    explanation_parts.append(f"🎊 Great news! You are eligible for {eligible_count} scheme(s)!")
                else:
                    explanation_parts.append("💪 Don't worry! There are other options available.")
            
            # Specific recommendations based on user info
            monthly_income = user_info.get("monthly_income", 0)
            family_size = user_info.get("family_size", 0)
            location = user_info.get("location", "")
            
            if monthly_income > 0:
                explanation_parts.append("💰 Aapki Financial Situation:")
                if monthly_income <= 30000:
                    explanation_parts.append("   ✅ Aapki income kam hai, aap kai schemes ke liye eligible ho sakte hain")
                elif monthly_income <= 50000:
                    explanation_parts.append("   ✅ Aapki income moderate hai, kuch schemes available hain")
                else:
                    explanation_parts.append("   ⚠️ Aapki income zyada hai, limited options available hain")
                explanation_parts.append("")
            
            # General guidance
            explanation_parts.append("🆘 Additional Help:")
            explanation_parts.append("   📞 Helpline call kariye")
            explanation_parts.append("   🏛️ Local government office jaaiye")
            explanation_parts.append("   🌐 Online portal check kariye")
            explanation_parts.append("")
            explanation_parts.append("🤲 Allah aapki madad kare! InshaAllah sab theek ho jayega!")
            
            return "\n".join(explanation_parts)
            
        except Exception as e:
            return f"""
            Assalam-o-Alaikum! Main aapki madad kar raha hun.
            
            ⚠️ Technical issue: {str(e)}
            
            🔧 Agar aur help chahiye to:
            1. 📞 Helpline call kariye
            2. 🏛️ Local office jaaiye  
            3. 🌐 Online portal check kariye
            
            🤲 Allah aapki madad kare!
            """


class DocumentCollectionAgent:
    """Agent responsible for collecting required documents from users."""
    
    def __init__(self):
        if not FALLBACK_MODE and VERTEXAI_AVAILABLE and GenerativeModel:
            try:
                self.model = GenerativeModel("gemini-pro")
            except Exception as e:
                print(f"⚠️  Warning: Could not initialize Gemini model: {e}")
                self.model = None
        else:
            self.model = None
    
    def collect_documents(self, scheme_name: str, user_info: Dict[str, Any]) -> Dict[str, Any]:
        """Collect required documents for a specific scheme."""
        try:
            # Get scheme details from PolicyAgent
            policy_agent = PolicyAgent()
            scheme_details = self._find_scheme_details(scheme_name, policy_agent.policies)
            
            if not scheme_details:
                return {
                    "status": "error",
                    "message": "Scheme not found",
                    "required_documents": [],
                    "document_status": {}
                }
            
            required_docs = scheme_details.get("required_documents", [])
            document_status = {}
            
            # Check which documents user already has
            for doc in required_docs:
                document_status[doc] = {
                    "required": True,
                    "provided": False,
                    "status": "missing"
                }
            
            return {
                "status": "success",
                "scheme_name": scheme_name,
                "required_documents": required_docs,
                "document_status": document_status,
                "collection_message": f"To apply for {scheme_name}, you need to provide the following documents:"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error collecting document requirements: {str(e)}",
                "required_documents": [],
                "document_status": {}
            }
    
    def _find_scheme_details(self, scheme_name: str, policies: Dict) -> Dict:
        """Find scheme details from policies."""
        for category, schemes in policies.items():
            for scheme in schemes:
                if scheme["name"] == scheme_name:
                    return scheme
        return None
    
    def update_document_status(self, scheme_name: str, document_name: str, status: str) -> Dict[str, Any]:
        """Update the status of a specific document."""
        return {
            "status": "success",
            "message": f"Document {document_name} status updated to {status}",
            "document_name": document_name,
            "new_status": status
        }


class HelplineAgent:
    """Agent responsible for providing helpline information and forwarding queries."""
    
    def __init__(self):
        if not FALLBACK_MODE and VERTEXAI_AVAILABLE and GenerativeModel:
            try:
                self.model = GenerativeModel("gemini-pro")
            except Exception as e:
                print(f"⚠️  Warning: Could not initialize Gemini model: {e}")
                self.model = None
        else:
            self.model = None
        
        self.general_helplines = {
            "citizen_portal": "0800-12345",
            "ehsaas_program": "0800-26477",
            "government_services": "0800-98765",
            "emergency_support": "0800-11111"
        }
    
    def get_helpline_info(self, scheme_name: str = None, issue_type: str = None) -> Dict[str, Any]:
        """Get relevant helpline information based on scheme or issue type."""
        try:
            helplines = []
            
            if scheme_name:
                # Get scheme-specific helpline
                policy_agent = PolicyAgent()
                scheme_details = self._find_scheme_details(scheme_name, policy_agent.policies)
                if scheme_details and "helpline" in scheme_details:
                    helplines.append({
                        "name": scheme_name,
                        "number": scheme_details["helpline"],
                        "website": scheme_details.get("website", ""),
                        "type": "scheme_specific"
                    })
            
            # Add general helplines based on issue type
            if issue_type:
                if issue_type in ["education", "healthcare", "employment"]:
                    helplines.append({
                        "name": "Ehsaas Program Helpline",
                        "number": "0800-26477",
                        "website": "https://ehsaas.gov.pk",
                        "type": "general"
                    })
                
                helplines.append({
                    "name": "Citizen Portal Helpline",
                    "number": "0800-12345",
                    "website": "https://citizen.gov.pk",
                    "type": "general"
                })
            
            # Add emergency helpline if no specific helpline found
            if not helplines:
                helplines.append({
                    "name": "Government Services Helpline",
                    "number": "0800-98765",
                    "website": "https://gov.pk",
                    "type": "general"
                })
            
            return {
                "status": "success",
                "helplines": helplines,
                "message": "Here are the relevant helpline numbers for your query:"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error getting helpline information: {str(e)}",
                "helplines": []
            }
    
    def forward_query(self, user_issue: str, user_info: Dict[str, Any], department: str = None) -> Dict[str, Any]:
        """Forward user query to relevant department."""
        try:
            # Generate query reference number
            import time
            reference_number = f"QR{int(time.time())}"
            
            # Determine department if not provided
            if not department:
                department = self._determine_department(user_issue)
            
            return {
                "status": "success",
                "message": f"Your query has been forwarded to the {department} department",
                "reference_number": reference_number,
                "department": department,
                "estimated_response_time": "2-3 business days",
                "helpline": self.general_helplines.get("citizen_portal", "0800-12345"),
                "next_steps": [
                    "Keep your reference number safe",
                    "You will receive SMS/email updates",
                    "Contact helpline if no response within 3 days"
                ]
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error forwarding query: {str(e)}",
                "reference_number": None
            }
    
    def _find_scheme_details(self, scheme_name: str, policies: Dict) -> Dict:
        """Find scheme details from policies."""
        for category, schemes in policies.items():
            for scheme in schemes:
                if scheme["name"] == scheme_name:
                    return scheme
        return None
    
    def _determine_department(self, user_issue: str) -> str:
        """Determine relevant department based on user issue."""
        issue_lower = user_issue.lower()
        
        if any(word in issue_lower for word in ["education", "school", "student", "study"]):
            return "Education Department"
        elif any(word in issue_lower for word in ["health", "medical", "hospital", "treatment"]):
            return "Health Department"
        elif any(word in issue_lower for word in ["house", "housing", "home", "property"]):
            return "Housing Department"
        elif any(word in issue_lower for word in ["job", "employment", "work", "income"]):
            return "Labor Department"
        else:
            return "General Services Department"


class ApplicationAssistantAgent:
    """Agent responsible for helping users apply for schemes."""
    
    def __init__(self):
        if not FALLBACK_MODE and VERTEXAI_AVAILABLE and GenerativeModel:
            try:
                self.model = GenerativeModel("gemini-pro")
            except Exception as e:
                print(f"⚠️  Warning: Could not initialize Gemini model: {e}")
                self.model = None
        else:
            self.model = None
    
    def assist_application(self, scheme_name: str, user_info: Dict[str, Any], documents: Dict[str, str] = None) -> Dict[str, Any]:
        """Assist user with scheme application process."""
        try:
            policy_agent = PolicyAgent()
            scheme_details = self._find_scheme_details(scheme_name, policy_agent.policies)
            
            if not scheme_details:
                return {
                    "status": "error",
                    "message": "Scheme not found",
                    "application_steps": []
                }
            
            # Check eligibility first
            eligibility_agent = EligibilityAgent()
            eligibility_result = eligibility_agent.check_eligibility(scheme_name, user_info)
            
            if not eligibility_result.get("eligible", False):
                return {
                    "status": "not_eligible",
                    "message": "You are not eligible for this scheme",
                    "reason": eligibility_result.get("reason", ""),
                    "missing_requirements": eligibility_result.get("missing_requirements", []),
                    "suggestions": eligibility_result.get("next_steps", [])
                }
            
            # Generate application steps
            application_steps = self._generate_application_steps(scheme_details, user_info, documents)
            
            return {
                "status": "success",
                "scheme_name": scheme_name,
                "application_steps": application_steps,
                "application_process": scheme_details.get("application_process", ""),
                "website": scheme_details.get("website", ""),
                "helpline": scheme_details.get("helpline", ""),
                "message": f"Great! You are eligible for {scheme_name}. Here's how to apply:"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error assisting with application: {str(e)}",
                "application_steps": []
            }
    
    def _find_scheme_details(self, scheme_name: str, policies: Dict) -> Dict:
        """Find scheme details from policies."""
        for category, schemes in policies.items():
            for scheme in schemes:
                if scheme["name"] == scheme_name:
                    return scheme
        return None
    
    def _generate_application_steps(self, scheme_details: Dict, user_info: Dict, documents: Dict) -> List[str]:
        """Generate step-by-step application process."""
        steps = []
        
        # Step 1: Document preparation
        required_docs = scheme_details.get("required_documents", [])
        if required_docs:
            steps.append("📋 Prepare Required Documents:")
            for doc in required_docs:
                steps.append(f"   • {doc}")
        
        # Step 2: Online application
        if "online" in scheme_details.get("application_process", "").lower():
            steps.append("💻 Apply Online:")
            steps.append("   • Visit the official website")
            steps.append("   • Create an account")
            steps.append("   • Fill out the application form")
            steps.append("   • Upload required documents")
            steps.append("   • Submit application")
        
        # Step 3: Verification
        steps.append("✅ Verification Process:")
        steps.append("   • Documents will be verified")
        steps.append("   • You may be contacted for additional information")
        steps.append("   • Application status can be checked online")
        
        # Step 4: Approval
        steps.append("🎉 After Approval:")
        steps.append("   • You will receive notification via SMS/email")
        steps.append("   • Benefits will be disbursed as per scheme rules")
        steps.append("   • Keep your application reference number safe")
        
        return steps


class AgentOrchestrator:
    """Orchestrates multiple agents to solve user issues."""
    
    def __init__(self):
        self.policy_agent = PolicyAgent()
        self.eligibility_agent = EligibilityAgent()
        self.explanation_agent = ExplanationAgent()
        self.document_agent = DocumentCollectionAgent()
        self.helpline_agent = HelplineAgent()
        self.application_agent = ApplicationAssistantAgent()
    
    def solve_user_issue(self, user_issue: str, user_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """Main method to solve user issues using multiple agents."""
        if user_info is None:
            user_info = {}
        
        # Step 1: Policy Agent analyzes the issue
        policy_analysis = self.policy_agent.analyze_user_issue(user_issue)
        
        # Step 2: Eligibility Agent checks eligibility for relevant schemes
        eligibility_results = []
        scheme_details = []
        document_requirements = []
        
        for scheme in policy_analysis.get("relevant_schemes", []):
            eligibility = self.eligibility_agent.check_eligibility(scheme, user_info)
            eligibility_results.append({
                "scheme": scheme,
                "eligibility": eligibility
            })
        
            # Get detailed scheme information
            scheme_detail = self._get_scheme_details(scheme)
            if scheme_detail:
                scheme_details.append(scheme_detail)
                
                # Get document requirements for eligible schemes
                if eligibility.get("eligible", False):
                    doc_result = self.document_agent.collect_documents(scheme, user_info)
                    if doc_result.get("status") == "success":
                        document_requirements.append({
                            "scheme": scheme,
                            "documents": doc_result.get("required_documents", []),
                            "message": doc_result.get("collection_message", "")
                        })
        
        # Step 3: Get helpline information
        helpline_info = self.helpline_agent.get_helpline_info(
            scheme_name=policy_analysis.get("relevant_schemes", [None])[0] if policy_analysis.get("relevant_schemes") else None,
            issue_type=policy_analysis.get("issue_type")
        )
        
        # Step 4: Explanation Agent creates final explanation
        explanation_data = {
            "issue_analysis": policy_analysis,
            "eligibility_results": eligibility_results,
            "user_info": user_info
        }
        
        final_explanation = self.explanation_agent.explain_in_plain_language(explanation_data)
        
        # Step 5: Generate comprehensive response
        response = {
            "status": "success",
            "issue_analysis": policy_analysis,
            "eligibility_results": eligibility_results,
            "scheme_details": scheme_details,
            "document_requirements": document_requirements,
            "helpline_info": helpline_info,
            "explanation": final_explanation,
            "recommendations": self._generate_recommendations(eligibility_results),
            "next_actions": self._generate_next_actions(eligibility_results, document_requirements)
        }
        
        return response
    
    def _get_scheme_details(self, scheme_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific scheme."""
        for category, schemes in self.policy_agent.policies.items():
            for scheme in schemes:
                if scheme["name"] == scheme_name:
                    return {
                        "name": scheme["name"],
                        "description": scheme["description"],
                        "benefits": scheme.get("benefits", ""),
                        "application_process": scheme.get("application_process", ""),
                        "helpline": scheme.get("helpline", ""),
                        "website": scheme.get("website", ""),
                        "category": category.replace("_schemes", "").title()
                    }
        return None
    
    def _generate_next_actions(self, eligibility_results: List[Dict], document_requirements: List[Dict]) -> List[str]:
        """Generate next action steps for the user."""
        actions = []
        
        # Check if user is eligible for any scheme
        eligible_schemes = [result for result in eligibility_results if result["eligibility"].get("eligible", False)]
        
        if eligible_schemes:
            actions.append("🎯 You are eligible for some schemes! Consider applying.")
            actions.append("📋 Check the required documents for each eligible scheme.")
            actions.append("💻 Visit the official websites to start your application.")
            actions.append("📞 Contact helplines if you need assistance with the application process.")
        else:
            actions.append("📞 Contact the helpline numbers provided for personalized assistance.")
            actions.append("🏛️ Visit your local government office for alternative options.")
            actions.append("🌐 Check other government schemes that might be suitable.")
        
        actions.append("📱 Keep your reference number safe if you contact helplines.")
        
        return actions
    
    def _generate_recommendations(self, eligibility_results: List[Dict]) -> List[str]:
        """Generate actionable recommendations based on eligibility results."""
        recommendations = []
        
        for result in eligibility_results:
            if result["eligibility"]["eligible"]:
                recommendations.append(f"[ELIGIBLE] Apply for {result['scheme']} - You are eligible!")
            else:
                recommendations.append(f"[NOT ELIGIBLE] {result['scheme']} - Not eligible: {result['eligibility']['reason']}")
        
        if not recommendations:
            recommendations.append("Contact your local government office for personalized assistance")
            recommendations.append("Check online government portals for more schemes")
        
        return recommendations


# Test function
if __name__ == "__main__":
    orchestrator = AgentOrchestrator()
    
    # Test case
    test_issue = "I need help with my children's education expenses. My monthly income is 25,000 and I have 3 children."
    test_user_info = {
        "monthly_income": 25000,
        "number_of_children": 3,
        "children_ages": [8, 12, 15],
        "location": "Karachi"
    }
    
    result = orchestrator.solve_user_issue(test_issue, test_user_info)
    print("=== AGENT ORCHESTRATION RESULT ===")
    try:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except UnicodeEncodeError:
        # Fallback for Windows console
        print(json.dumps(result, indent=2, ensure_ascii=True))
