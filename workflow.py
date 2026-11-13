"""Lesson-specific workflow. Read this file before the execution adapter."""
from __future__ import annotations
import asyncio
import json
from pathlib import Path
from runtime import atomic_json, contained_path, in_process_tool

async def run(agent, data):
    question = data['question']
    complexity = len(question.split()) + 5 * int('compare' in question.lower())
    strategy = 'reviewed' if complexity >= data['complexity_cutoff'] else 'simple'
    answer = await agent.ask('answer', 'Answer this question and state assumptions.', {'question': question, 'strategy': strategy}, 'Compare evidence and constraints before selecting an alternative.')
    review = None
    if strategy == 'reviewed':
        review = await agent.ask('review', 'Check coverage and flag unsupported recommendations.', {'question': question, 'answer': answer}, {'covered': True, 'issue': 'Specific alternatives still need supplied evidence.'})
    return {'complexity_heuristic': complexity, 'strategy': strategy, 'answer': answer, 'review': review, 'calls': agent.calls}
