# Reflection

The supplied handout explains the lab outcomes and lists the technical deliverables, but it does not include the four reflection prompts mentioned by the assignment repository README. These responses cover the four expected reflection areas.

1. **What kinds of issues did static analysis identify?**  
   Bandit found a high-severity shell invocation risk, a medium-severity SQL construction risk, and a low-severity swallowed exception. Pylint highlighted global state, inconsistent names, missing documentation, an unused argument, and long lines. Flake8 confirmed the spacing and line-length problems.

2. **Which findings mattered most, and why?**  
   The shell command and SQL construction mattered most because untrusted supplier or item values could affect command execution or database queries. Replacing the shell call and parameterizing SQL removes those risky paths. The swallowed exception was also removed so database failures are visible.

3. **What changed after the fixes?**  
   Order quantity is now calculated from the database instead of a global variable, input values are validated, and the names and documentation are clearer. The demonstration still records two orders, marks one received, prints the remaining count and total quantity, and cleans up received orders.

4. **How did static analysis contribute to maintainability and security?**  
   The tools provided concrete, repeatable feedback before and after editing. Bandit focused attention on risky APIs, while Pylint and Flake8 improved structure and consistency. The final reports show a 10.00/10 Pylint score, no Bandit findings, and no Flake8 violations. Static analysis does not prove that a program is free of defects, but it catches common problems early and helps keep fixes verifiable.
