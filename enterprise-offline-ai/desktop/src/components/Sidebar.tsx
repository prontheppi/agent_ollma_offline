const items = ["Dashboard", "Chat", "Upload Documents", "Documents", "Settings", "Admin"];

export function Sidebar() {
  return (
    <aside className="sidebar">
      <strong>EnterpriseOfflineAI</strong>
      <nav>
        {items.map((item) => (
          <button key={item} type="button">
            {item}
          </button>
        ))}
      </nav>
    </aside>
  );
}
