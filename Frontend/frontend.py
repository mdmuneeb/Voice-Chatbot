from __future__ import annotations

from typing import Any

import requests
import streamlit as st


DEFAULT_API_BASE = "http://127.0.0.1:8000"
REQUEST_TIMEOUT = 90


def init_state() -> None:
	if "api_base" not in st.session_state:
		st.session_state.api_base = DEFAULT_API_BASE

	if "threads" not in st.session_state:
		st.session_state.threads = []

	if "active_thread_id" not in st.session_state:
		st.session_state.active_thread_id = None

	if "chat_history" not in st.session_state:
		st.session_state.chat_history = {}

	if "threads_loaded" not in st.session_state:
		st.session_state.threads_loaded = False

	if "loaded_thread_ids" not in st.session_state:
		st.session_state.loaded_thread_ids = set()


def api_get(path: str) -> tuple[bool, Any]:
	base_url = st.session_state.api_base.rstrip("/")

	try:
		response = requests.get(
			f"{base_url}{path}",
			timeout=REQUEST_TIMEOUT,
		)
		response.raise_for_status()
		return True, response.json()
	except requests.RequestException as exc:
		return False, str(exc)


def api_post(path: str, payload: dict[str, Any]) -> tuple[bool, Any]:
	base_url = st.session_state.api_base.rstrip("/")

	try:
		response = requests.post(
			f"{base_url}{path}",
			json=payload,
			timeout=REQUEST_TIMEOUT,
		)
		response.raise_for_status()
		return True, response.json()
	except requests.RequestException as exc:
		return False, str(exc)


def load_threads() -> None:
	success, result = api_get("/api/threads")

	if not success:
		st.sidebar.error(f"Could not load threads: {result}")
		return

	st.session_state.threads = result

	if st.session_state.active_thread_id is None and result:
		st.session_state.active_thread_id = result[0]["id"]

	for thread in result:
		st.session_state.chat_history.setdefault(thread["id"], [])


def create_thread(title: str) -> None:
	payload = {"title": title or "New Chat"}
	success, result = api_post("/api/threads", payload)

	if not success:
		st.sidebar.error(f"Could not create thread: {result}")
		return

	st.session_state.threads.insert(0, result)
	st.session_state.active_thread_id = result["id"]
	st.session_state.chat_history.setdefault(result["id"], [])
	st.session_state.loaded_thread_ids.add(result["id"])
	st.sidebar.success("Thread created")


def extract_messages(thread_payload: Any) -> list[dict[str, Any]]:
	if isinstance(thread_payload, list):
		return [item for item in thread_payload if isinstance(item, dict)]

	if not isinstance(thread_payload, dict):
		return []

	messages = thread_payload.get("messages")
	if isinstance(messages, list):
		return [item for item in messages if isinstance(item, dict)]

	data = thread_payload.get("data")
	if isinstance(data, dict):
		data_messages = data.get("messages")
		if isinstance(data_messages, list):
			return [item for item in data_messages if isinstance(item, dict)]

	return []


def load_thread_history(thread_id: str, force: bool = False) -> None:
	if not force and thread_id in st.session_state.loaded_thread_ids:
		return

	success, result = api_get(f"/api/threads/{thread_id}")
	if not success:
		# Keep local in-session messages if history endpoint is unavailable.
		st.session_state.chat_history.setdefault(thread_id, [])
		return

	raw_messages = extract_messages(result)

	if not raw_messages:
		st.session_state.chat_history.setdefault(thread_id, [])
		st.session_state.loaded_thread_ids.add(thread_id)
		return

	normalized: list[dict[str, Any]] = []
	for message in raw_messages:
		role = message.get("role")
		if role not in {"user", "assistant"}:
			continue

		content = message.get("content") or message.get("message") or ""
		audio_url = message.get("audio_url")

		normalized.append(
			{
				"role": role,
				"content": str(content),
				"audio_url": audio_url,
			}
		)

	st.session_state.chat_history[thread_id] = normalized
	st.session_state.loaded_thread_ids.add(thread_id)


def render_sidebar() -> bool:
	st.sidebar.header("Settings")

	st.session_state.api_base = st.sidebar.text_input(
		"Backend API Base URL",
		value=st.session_state.api_base,
		help="Example: http://127.0.0.1:8000",
	)

	if st.sidebar.button("Refresh Threads", use_container_width=True):
		load_threads()

	st.sidebar.divider()
	st.sidebar.subheader("New Conversation")

	new_title = st.sidebar.text_input(
		"Chat title",
		value="New Chat",
	)

	if st.sidebar.button("Create chat", use_container_width=True):
		create_thread(new_title)

	st.sidebar.divider()
	st.sidebar.subheader("Chats")

	if not st.session_state.threads:
		st.sidebar.info("No chats yet. Create one to start chatting.")
		return False

	options = [thread["id"] for thread in st.session_state.threads]
	labels = {
		thread["id"]: thread.get("title") or "Untitled"
		for thread in st.session_state.threads
	}

	current = st.session_state.active_thread_id
	if current not in options:
		current = options[0]
		st.session_state.active_thread_id = current

	selected = st.sidebar.radio(
		"Select chat",
		options=options,
		index=options.index(current),
		format_func=lambda thread_id: labels.get(thread_id, thread_id),
	)

	changed = selected != st.session_state.active_thread_id
	st.session_state.active_thread_id = selected
	return changed


def render_messages(thread_id: str) -> None:
	history = st.session_state.chat_history.get(thread_id, [])

	for message in history:
		role = message.get("role", "assistant")

		with st.chat_message("user" if role == "user" else "assistant"):
			st.markdown(message.get("content", ""))

			if role == "assistant" and message.get("audio_url"):
				st.audio(message["audio_url"], format="audio/wav")


def handle_user_message(thread_id: str, prompt: str) -> None:
	st.session_state.chat_history[thread_id].append(
		{
			"role": "user",
			"content": prompt,
			"audio_url": None,
		}
	)

	payload = {
		"thread_id": thread_id,
		"message": prompt,
	}

	with st.spinner("Thinking and generating audio..."):
		success, result = api_post("/api/chat", payload)

	if not success:
		st.session_state.chat_history[thread_id].append(
			{
				"role": "assistant",
				"content": f"Backend error: {result}",
				"audio_url": None,
			}
		)
		return

	st.session_state.chat_history[thread_id].append(
		{
			"role": "assistant",
			"content": result.get("response", ""),
			"audio_url": result.get("audio_url"),
		}
	)


def main() -> None:
	st.set_page_config(
		page_title="Voice Chatbot",
		page_icon="🎙️",
		layout="wide",
	)

	init_state()

	if not st.session_state.threads_loaded:
		load_threads()
		st.session_state.threads_loaded = True

	chat_changed = render_sidebar()

	st.title("Voice Chatbot")
	st.caption("Chat with your backend model and play generated speech.")

	active_thread_id = st.session_state.active_thread_id

	if not active_thread_id:
		st.info("Create a thread from the sidebar to start chatting.")
		return

	if chat_changed or active_thread_id not in st.session_state.loaded_thread_ids:
		load_thread_history(active_thread_id)

	render_messages(active_thread_id)

	user_prompt = st.chat_input("Type your message")
	if user_prompt:
		handle_user_message(active_thread_id, user_prompt)
		st.rerun()


if __name__ == "__main__":
	main()
