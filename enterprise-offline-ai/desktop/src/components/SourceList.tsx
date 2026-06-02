export type Source = {
  file_name: string;
  page_number?: number;
  chunk_index: number;
  excerpt: string;
};

export function SourceList({ sources }: { sources: Source[] }) {
  return (
    <ul className="source-list">
      {sources.map((source) => (
        <li key={`${source.file_name}-${source.chunk_index}`}>
          <strong>{source.file_name}</strong>
          {source.page_number ? ` page ${source.page_number}` : ""}: {source.excerpt}
        </li>
      ))}
    </ul>
  );
}
