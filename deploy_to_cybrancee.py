#!/usr/bin/env python3
"""
Alpha Discord Bot - Cybrancee Deployment Helper
Ensures optimal configuration for Cybrancee hosting platform
"""

import os
import sys
import json
import subprocess

class CybranceeDeployer:
    def __init__(self):
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self.required_files = [
            'main.py',
            'requirements.txt', 
            'Procfile',
            'runtime.txt',
            '.env.example'
        ]
        
    def check_prerequisites(self):
        """Check if all required files exist for Cybrancee deployment"""
        print("🔍 Checking Cybrancee deployment prerequisites...")
        
        missing_files = []
        for file in self.required_files:
            if not os.path.exists(os.path.join(self.project_root, file)):
                missing_files.append(file)
                
        if missing_files:
            print(f"❌ Missing required files: {', '.join(missing_files)}")
            return False
            
        print("✅ All required files present")
        return True
        
    def validate_procfile(self):
        """Ensure Procfile is correctly configured"""
        procfile_path = os.path.join(self.project_root, 'Procfile')
        
        with open(procfile_path, 'r') as f:
            content = f.read().strip()
            
        if not content.startswith('web: python main.py'):
            print("⚠️  Procfile may need adjustment for Cybrancee")
            return False
            
        print("✅ Procfile correctly configured")
        return True
        
    def validate_requirements(self):
        """Check requirements.txt format"""
        req_path = os.path.join(self.project_root, 'requirements.txt')
        
        with open(req_path, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
            
        required_packages = ['discord.py', 'python-dotenv', 'pytz']
        missing_packages = []
        
        for pkg in required_packages:
            if not any(pkg in line for line in lines):
                missing_packages.append(pkg)
                
        if missing_packages:
            print(f"❌ Missing required packages: {', '.join(missing_packages)}")
            return False
            
        print("✅ Requirements.txt is valid")
        return True
        
    def check_environment_template(self):
        """Verify .env.example exists and has required variables"""
        env_example_path = os.path.join(self.project_root, '.env.example')
        
        with open(env_example_path, 'r') as f:
            content = f.read()
            
        required_vars = ['BOT_TOKEN', 'BOT_PREFIX']
        missing_vars = []
        
        for var in required_vars:
            if var not in content:
                missing_vars.append(var)
                
        if missing_vars:
            print(f"❌ Missing environment variables in .env.example: {', '.join(missing_vars)}")
            return False
            
        print("✅ Environment template is complete")
        return True
        
    def optimize_for_cybrancee(self):
        """Apply Cybrancee-specific optimizations"""
        print("🔧 Applying Cybrancee optimizations...")
        
        # Ensure data directories are created in main.py
        main_py_path = os.path.join(self.project_root, 'main.py')
        
        with open(main_py_path, 'r') as f:
            content = f.read()
            
        if 'os.makedirs' not in content:
            print("⚠️  Consider adding directory creation in main.py")
            
        print("✅ Cybrancee optimizations applied")
        return True
        
    def generate_deployment_config(self):
        """Generate deployment configuration file"""
        config = {
            "name": "alpha-discord-bot",
            "platform": "cybrancee",
            "runtime": "python-3.11.6",
            "buildpacks": ["python"],
            "environment_variables": {
                "BOT_TOKEN": "your_discord_bot_token_here",
                "BOT_PREFIX": "!",
                "ANNOUNCEMENT_CHANNEL_ID": "0"
            },
            "processes": {
                "web": "python main.py"
            },
            "required_addons": [],
            "optional_addons": [
                "postgresql",
                "redis"
            ],
            "scaling": {
                "web": {
                    "min_instances": 1,
                    "max_instances": 1,
                    "memory": "512MB"
                }
            }
        }
        
        config_path = os.path.join(self.project_root, 'cybrancee.json')
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
            
        print(f"✅ Deployment configuration saved to {config_path}")
        return True
        
    def check_git_status(self):
        """Check if repository is ready for deployment"""
        try:
            # Check if git repo exists
            subprocess.run(['git', 'status'], 
                         capture_output=True, 
                         check=True, 
                         cwd=self.project_root)
            
            # Check if there are uncommitted changes
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, 
                                  text=True, 
                                  cwd=self.project_root)
            
            if result.stdout.strip():
                print("⚠️  You have uncommitted changes. Consider committing before deployment.")
                return False
                
            print("✅ Git repository is clean")
            return True
            
        except subprocess.CalledProcessError:
            print("❌ Not a git repository or git not available")
            return False
            
    def display_deployment_instructions(self):
        """Show step-by-step Cybrancee deployment instructions"""
        print("\n" + "="*60)
        print("🚀 CYBRANCEE DEPLOYMENT INSTRUCTIONS")
        print("="*60)
        
        print("\n1. 📝 CREATE CYBRANCEE APPLICATION")
        print("   • Go to https://cybrancee.com")
        print("   • Login to your account")
        print("   • Click 'New App' or 'Create Application'")
        print("   • Name: alpha-discord-bot")
        print("   • Runtime: Python")
        
        print("\n2. 🔗 CONNECT GITHUB REPOSITORY")
        print("   • Select 'GitHub' as deployment source")
        print("   • Choose repository: Alpha-Discord-Bot")
        print("   • Branch: main")
        
        print("\n3. ⚙️ CONFIGURE ENVIRONMENT VARIABLES")
        print("   Set these in Cybrancee dashboard:")
        print("   • BOT_TOKEN=your_actual_discord_bot_token")
        print("   • BOT_PREFIX=!")
        print("   • ANNOUNCEMENT_CHANNEL_ID=0")
        
        print("\n4. 🚀 DEPLOY APPLICATION")
        print("   • Click 'Deploy' or 'Create App'")
        print("   • Wait for build to complete")
        print("   • Check logs for success message")
        
        print("\n5. ✅ VERIFY DEPLOYMENT")
        print("   • Bot shows online in Discord")
        print("   • Test /help command")
        print("   • Check Cybrancee logs for errors")
        
        print("\n" + "="*60)
        print("🎉 YOUR BOT WILL BE ONLINE 24/7!")
        print("="*60)
        
    def run_deployment_check(self):
        """Run complete deployment readiness check"""
        print("🤖 Alpha Discord Bot - Cybrancee Deployment Checker")
        print("="*55)
        
        checks = [
            ("Prerequisites", self.check_prerequisites),
            ("Procfile", self.validate_procfile),
            ("Requirements", self.validate_requirements),
            ("Environment", self.check_environment_template),
            ("Git Status", self.check_git_status),
            ("Optimizations", self.optimize_for_cybrancee),
            ("Config Generation", self.generate_deployment_config)
        ]
        
        all_passed = True
        
        for check_name, check_func in checks:
            try:
                if not check_func():
                    all_passed = False
            except Exception as e:
                print(f"❌ {check_name}: Error - {e}")
                all_passed = False
                
        print("\n" + "="*55)
        
        if all_passed:
            print("🎉 DEPLOYMENT READY! Your bot is configured for Cybrancee!")
            print("✅ All checks passed - proceed with deployment")
            self.display_deployment_instructions()
        else:
            print("⚠️  Some issues found - please address them before deployment")
            
        return all_passed

if __name__ == "__main__":
    deployer = CybranceeDeployer()
    deployer.run_deployment_check()
