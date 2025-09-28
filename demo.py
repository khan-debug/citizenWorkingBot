#!/usr/bin/env python3
"""
Demo script to show the improved Citizen Bot Pakistan system
"""

from multi_agents import AgentOrchestrator
import json

def demo_education_issue():
    """Demonstrate the system with an education issue."""
    print("=" * 60)
    print("CITIZEN BOT PAKISTAN - DEMO")
    print("=" * 60)
    print()
    
    orchestrator = AgentOrchestrator()
    
    # Test case 1: Education issue
    print("TEST CASE 1: Education Issue")
    print("-" * 40)
    
    test_issue = "I need help with my children's education expenses. My monthly income is 25,000 PKR and I have 3 children aged 8, 12, and 15."
    test_user_info = {
        "monthly_income": 25000,
        "family_size": 3,
        "children_ages": [8, 12, 15],
        "location": "Karachi",
        "issue_type": "education"
    }
    
    print(f"User Issue: {test_issue}")
    print(f"User Info: {test_user_info}")
    print()
    
    result = orchestrator.solve_user_issue(test_issue, test_user_info)
    
    print("AI RESPONSE:")
    print("-" * 40)
    print(result["explanation"])
    print()
    
    print("RECOMMENDATIONS:")
    print("-" * 40)
    for rec in result["recommendations"]:
        print(f"  {rec}")
    print()
    
    return result

def demo_housing_issue():
    """Demonstrate the system with a housing issue."""
    print("TEST CASE 2: Housing Issue")
    print("-" * 40)
    
    orchestrator = AgentOrchestrator()
    
    test_issue = "I want to buy a house but I don't have enough money. My monthly income is 35,000 PKR and I have a family of 4."
    test_user_info = {
        "monthly_income": 35000,
        "family_size": 4,
        "location": "Lahore",
        "issue_type": "housing"
    }
    
    print(f"User Issue: {test_issue}")
    print(f"User Info: {test_user_info}")
    print()
    
    result = orchestrator.solve_user_issue(test_issue, test_user_info)
    
    print("AI RESPONSE:")
    print("-" * 40)
    print(result["explanation"])
    print()
    
    print("RECOMMENDATIONS:")
    print("-" * 40)
    for rec in result["recommendations"]:
        print(f"  {rec}")
    print()
    
    return result

def demo_employment_issue():
    """Demonstrate the system with an employment issue."""
    print("TEST CASE 3: Employment Issue")
    print("-" * 40)
    
    orchestrator = AgentOrchestrator()
    
    test_issue = "I lost my job and need financial help. My monthly income is now only 15,000 PKR and I have 2 children."
    test_user_info = {
        "monthly_income": 15000,
        "family_size": 3,
        "location": "Islamabad",
        "issue_type": "employment"
    }
    
    print(f"User Issue: {test_issue}")
    print(f"User Info: {test_user_info}")
    print()
    
    result = orchestrator.solve_user_issue(test_issue, test_user_info)
    
    print("AI RESPONSE:")
    print("-" * 40)
    print(result["explanation"])
    print()
    
    print("RECOMMENDATIONS:")
    print("-" * 40)
    for rec in result["recommendations"]:
        print(f"  {rec}")
    print()
    
    return result

if __name__ == "__main__":
    try:
        # Run all demos
        demo_education_issue()
        demo_housing_issue()
        demo_employment_issue()
        
        print("=" * 60)
        print("DEMO COMPLETED SUCCESSFULLY!")
        print("To use the web interface, run: python app.py")
        print("Then open: http://localhost:5000")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error running demo: {e}")
        print("Make sure all dependencies are installed and Google Cloud is configured.")
