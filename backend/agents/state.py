from typing import TypedDict, List, Dict, Any, Optional

class AgentState(TypedDict):
    issue_number: int
    issue_data: Dict[str, Any]
    plan: List[str]
    needs_clarification: bool
    clarification_question: Optional[str]
    operator_response: Optional[str]
    investigation_notes: str
    changes_made: List[str]
    test_results: str
    review_comments: str
    pr_url: Optional[str]
    current_step: str
    error_info: Optional[Dict[str, Any]]
    steps_count: int
    tokens_used: int
    max_steps: int
    max_tokens: int
    messages: List[Dict[str, Any]]
