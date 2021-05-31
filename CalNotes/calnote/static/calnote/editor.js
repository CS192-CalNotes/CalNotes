function render() {
  const editor = document.getElementById("note-editor");
  const viewer = document.getElementById("note-viewer");
  try {
    viewer.innerHTML = marked(editor.value);
  } catch (err) {
    console.error(err.message, err.name);
  }
}

function initEditor() {
  const editor = document.getElementById("note-editor");
  if (!editor) return; // Not in /editNote page
  editor.addEventListener("input", (e) => {
    setTimeout(() => {
      render();
    }, 1);
  });
  editor.addEventListener("change", (e) => {
    setTimeout(() => {
      render();
    }, 1);
  });
  render();
}

initEditor();
