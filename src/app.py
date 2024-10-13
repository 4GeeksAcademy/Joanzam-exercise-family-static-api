"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
CORS(app)

# Create an instance of FamilyStructure
jackson_family = FamilyStructure('Jackson')

# Endpoint to retrieve all family members
@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

# Endpoint to retrieve a specific family member by ID
@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    return jsonify({"error": "Member not found"}), 404

# Endpoint to add a new family member
@app.route('/member', methods=['POST'])
def add_member():
    new_member = request.json
    if not new_member or 'first_name' not in new_member or 'age' not in new_member or 'lucky_numbers' not in new_member:
        return jsonify({"error": "Invalid request body"}), 400
    jackson_family.add_member(new_member)
    return jsonify({"message": "Member added successfully"}), 200

# Endpoint to delete a family member by ID
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        jackson_family.delete_member(member_id)
        return jsonify({"done": True}), 200
    return jsonify({"error": "Member not found"}), 404

# Sitemap generator for this API
@app.route('/')
def sitemap():
    return generate_sitemap(app)

if __name__ == '__main__':
    app.run(debug=True)
