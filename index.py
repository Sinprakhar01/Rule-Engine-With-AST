from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import json,re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://USERNAME:PASSWORD@localhost/rule_engine'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Node model
class Node(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    left_id = db.Column(db.Integer, db.ForeignKey('node.id'), nullable=True)
    right_id = db.Column(db.Integer, db.ForeignKey('node.id'), nullable=True)
    value = db.Column(db.Text, nullable=False)

    left = db.relationship('Node', remote_side=[id], backref='left_child', foreign_keys=[left_id])
    right = db.relationship('Node', remote_side=[id], backref='right_child', foreign_keys=[right_id])

    def __repr__(self):
        return f'<Node type={self.type}, value={self.value}>'

# Error handling helper
def handle_error(error):
    print(f"Error: {error}")
    return jsonify({"error": str(error)}), 500

def serialize_ast(node):
    """Recursively serialize the AST to a dictionary format."""
    if node is None:
        return None
    serialized_node = {
        "id": node.id,
        "type": node.type,
        "value": node.value,
        "left": serialize_ast(node.left),
        "right": serialize_ast(node.right),
    }
    return serialized_node

def parse_rule(rule_string):
    """Parse the rule string and construct the AST."""
    print(f"Parsing rule: {rule_string}")
    
    if "AND" in rule_string:
        operator_node = Node(type='operator', value='AND')
        db.session.add(operator_node)  # Add to session to get ID later
        conditions = rule_string.split("AND")
        print(conditions)
        left_node = parse_rule(conditions[0].strip())
        for i in range(1,len(conditions)):
            right_node = parse_rule(conditions[i].strip())
            operator_node.left_id = left_node.id
            operator_node.right_id = right_node.id
        db.session.commit()  # Commit to save operator_node ID
        return operator_node

    elif "OR" in rule_string:
        operator_node = Node(type='operator', value='OR')
        db.session.add(operator_node)  # Add to session to get ID later
        conditions = rule_string.split("OR")
        left_node = parse_rule(conditions[0].strip())
        right_node = parse_rule(conditions[1].strip())
        operator_node.left_id = left_node.id
        operator_node.right_id = right_node.id
        db.session.commit()  # Commit to save operator_node ID
        return operator_node

    else:
        # It's an operand (condition)
        operand_node = Node(type='operand', value=rule_string.strip())
        db.session.add(operand_node)
        db.session.commit()  # Commit to get the ID
        return operand_node

@app.route('/api/rules/create_rule', methods=['POST'])
def create_rule():
    try:
        data = request.json
        rule_string = data.get('rule_string')
        print(f"Received rule string: {rule_string}")
        rule_ast = parse_rule(rule_string)
        
        # Serialize the AST for response
        serialized_ast = serialize_ast(rule_ast)
        db.session.commit()  # Commit the operator node with its children
        print(f"Rule created with node ID: {rule_ast.id}")
        return jsonify({"message": "Rule created successfully", "ast": serialized_ast}), 201
    except Exception as e:
        return handle_error(e)

# API to combine rules
@app.route('/api/rules/combine_rules', methods=['POST'])
def combine_rules():
    try:
        rule_strings = request.json.get('rules', [])
        combined_ast = None
        for rule_string in rule_strings:
            rule_ast = parse_rule(rule_string)
            if combined_ast is None:
                combined_ast = rule_ast
            else:
                # Combine the current AST with the combined AST using AND logic
                new_combined_node = Node(type='operator', value='AND', left_id=combined_ast.id, right_id=rule_ast.id)
                db.session.add(new_combined_node)
                db.session.commit()
                combined_ast=new_combined_node # Commit after adding the new combined node
        serialized_ast = serialize_ast(combined_ast)
        return jsonify({"message": "Rules combined successfully", "ast": serialized_ast}), 201
    except Exception as e:
        return handle_error(e)


@app.route('/api/rules/evaluate_rule', methods=['POST'])
def evaluate_rule():
    try:
        data = request.json
        ast_id = data.get("ast_id")  # Get the AST ID from JSON
        user_data = data.get("user_data")  # Get the user data

        if ast_id is None or user_data is None:
            return jsonify({"error": "AST ID and user data are required"}), 400

        root_node = db.session.get(Node,ast_id)  # Retrieve the AST based on the AST ID
        if not root_node:
            return jsonify({"error": "Invalid AST ID"}), 404

        # Call the function to evaluate the rule here, passing the root node and user data
        result = evaluate_ast(root_node, user_data)

        return jsonify({"result": result}), 200

    except Exception as e:
        return handle_error(e)


def evaluate_ast(node, user_data):
    if node is None:
        return False

    # If the node is an operand, evaluate the condition
    if node.type == 'operand':
        condition = node.value.strip()
        # Regex to extract the variable, operator, and value
        match = re.match(r"\(*\s*([a-zA-Z_]+)\s*(>|<|=|>=|<=|!=)\s*([0-9]+|'[^']+')\s*\)*", condition)
        if not match:
            raise ValueError(f"Invalid condition: {condition}")

        var, operator, value = match.groups()
        if var not in user_data:
            raise ValueError(f"Missing required data: {var}")

        # Convert value to appropriate type
        if value.isdigit():
            value = int(value)
        elif value.startswith("'") and value.endswith("'"):
            value = value.strip("'")
        
        # Get the actual user data value
        user_value = user_data[var]

        # Apply the operator
        if operator == '>':
            return user_value > value
        elif operator == '<':
            return user_value < value
        elif operator == '=':
            return user_value == value
        elif operator == '>=':
            return user_value >= value
        elif operator == '<=':
            return user_value <= value
        elif operator == '!=':
            return user_value != value
        else:
            raise ValueError(f"Unsupported operator: {operator}")

    # If the node is an operator, recursively evaluate the left and right branches
    elif node.type == 'operator':
        left_result = evaluate_ast(node.left, user_data)
        right_result = evaluate_ast(node.right, user_data)

        if node.value == 'AND':
            return left_result and right_result
        elif node.value == 'OR':
            return left_result or right_result
        else:
            raise ValueError(f"Unsupported operator: {node.value}")

    return False

    

@app.route('/')
def display_ast():
    return render_template('ast_display.html')

# Main entry point
if __name__ == '__main__':
    with app.app_context():  # Use application context
        try:
            db.create_all()  # Create the tables inside the app context
            print("Database tables created successfully.")
        except Exception as e:
            print(f"Error creating tables: {e}")
    
    app.run(debug=True)
