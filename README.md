<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

<h1>Rule Engine with Abstract Syntax Tree (AST) in Flask</h1>

<p>This project is a Rule Engine built with Flask, allowing users to create, combine, and evaluate rules represented as an Abstract Syntax Tree (AST). Users can define logical conditions and evaluate them based on custom user data.</p>

<h2>Features</h2>
<ul>
    <li><strong>Create Rules</strong>: Users can define rules using logical operators (<code>AND</code>, <code>OR</code>) and conditions.</li>
    <li><strong>Combine Rules</strong>: Multiple rules can be combined using <code>AND</code> logic to create complex rules.</li>
    <li><strong>Evaluate Rules</strong>: Given user data, rules are evaluated based on the AST structure.</li>
</ul>

<h2>Table of Contents</h2>
<ul>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#dependencies">Dependencies</a></li>
    <li><a href="#database-setup">Database Setup</a></li>
    <li><a href="#running-the-application">Running the Application</a></li>
    <li><a href="#api-endpoints">API Endpoints</a></li>
    <li><a href="#design-choices">Design Choices</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
</ul>

<h2 id="installation">Installation</h2>

<h3>1. Clone the Repository</h3>
<pre><code>git clone https://github.com/yourusername/rule-engine-ast.git
cd rule-engine-ast
</code></pre>

<h3>2. Set Up Python Virtual Environment</h3>
<pre><code>python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
</code></pre>

<h3>3. Install Python Dependencies</h3>
<pre><code>pip install -r requirements.txt
</code></pre>


</code></pre>

<h4>Option B: Install MySQL Locally</h4>
<p>Install and configure MySQL to allow root access with password <code>root</code>. Create a database named <code>rule_engine</code>.</p>

<h3>5. Configure Environment Variables</h3>
<p>In <code>index.py</code>, update the <code>SQLALCHEMY_DATABASE_URI</code> as needed if not using default MySQL Docker setup.</p>

<h2 id="dependencies">Dependencies</h2>
<ul>
    <li><strong>Python 3.7+</strong></li>
    <li><strong>Flask</strong>: Web framework</li>
    <li><strong>Flask SQLAlchemy</strong>: ORM for database interaction</li>
    <li><strong>PyMySQL</strong>: MySQL client for SQLAlchemy</li>
    <li><strong>MySQL</strong>: Database server (running on localhost:3306)</li>
</ul>

<h2 id="database-setup">Database Setup</h2>
<p>In the <code>index.py</code> file, the database URI is configured as:</p>
<pre><code>app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/rule_engine'
</code></pre>

<pre><code>python index.py
</code></pre>
<p>The script will auto-create tables under the app context on the first run.</p>

<h2 id="running-the-application">Running the Application</h2>
<p>Run the Flask app:</p>
<pre><code>flask run
</code></pre>
<p>By default, it will be available at <a href="http://127.0.0.1:5000">http://127.0.0.1:5000</a>.</p>

<h2 id="api-endpoints">API Endpoints</h2>

<h3>1. Create Rule</h3>
<ul>
    <li><strong>Endpoint</strong>: <code>/api/rules/create_rule</code></li>
    <li><strong>Method</strong>: <code>POST</code></li>
    <li><strong>Payload</strong>: <code>{ "rule_string": "&lt;rule_logic&gt;" }</code></li>
    <li><strong>Description</strong>: Creates a rule and returns the generated AST.</li>
</ul>

<h3>2. Combine Rules</h3>
<ul>
    <li><strong>Endpoint</strong>: <code>/api/rules/combine_rules</code></li>
    <li><strong>Method</strong>: <code>POST</code></li>
    <li><strong>Payload</strong>: <code>{ "rules": ["&lt;rule_logic1&gt;", "&lt;rule_logic2&gt;", ...] }</code></li>
    <li><strong>Description</strong>: Combines multiple rules using <code>AND</code> logic and returns the AST.</li>
</ul>

<h3>3. Evaluate Rule</h3>
<ul>
    <li><strong>Endpoint</strong>: <code>/api/rules/evaluate_rule</code></li>
    <li><strong>Method</strong>: <code>POST</code></li>
    <li><strong>Payload</strong>: <code>{ "ast_id": &lt;AST_ID&gt;, "user_data": {&lt;user_data&gt;}}</code></li>
    <li><strong>Description</strong>: Evaluates the rule based on the user data.</li>
</ul>

<h2 id="design-choices">Design Choices</h2>
<ul>
    <li><strong>Flask Framework</strong>: Chosen for its simplicity and quick setup for building REST APIs.</li>
    <li><strong>SQLAlchemy with MySQL</strong>: SQLAlchemy ORM is used to interact with MySQL, supporting complex querying and transaction management.</li>
    <li><strong>Abstract Syntax Tree (AST)</strong>: AST is used to represent rules as a tree structure, allowing recursive evaluation based on operator precedence.</li>
    <li><strong>Dynamic Rule Parsing</strong>: The rule engine uses string parsing to construct AST nodes for <code>AND</code> and <code>OR</code> operators, allowing complex nested logic.</li>
</ul>

<h2 id="usage">Usage</h2>

<h3>Creating a Rule</h3>
<ol>
    <li>Enter a rule using logical operators like <code>AND</code> or <code>OR</code> (e.g., <code>age &gt; 30 AND salary &gt; 20000</code>).</li>
    <li>Click <strong>Create Rule</strong>. The AST will be displayed.</li>
</ol>

<h3>Combining Rules</h3>
<ol>
    <li>Enter one rule per line in the <strong>Combine Rules</strong> section.</li>
    <li>Click <strong>Combine Rules</strong> to merge rules with <code>AND</code> logic.</li>
</ol>

<h3>Evaluating a Rule</h3>
<ol>
    <li>Input a rule AST ID and user data fields such as <code>age</code>, <code>salary</code>, etc.</li>
    <li>Click <strong>Evaluate Rule</strong> to see if the rule is satisfied based on the provided data.</li>
</ol>

<h2 id="license">License</h2>
<p>This project is licensed under the MIT License.</p>

</body>
</html>
