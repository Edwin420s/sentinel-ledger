import { useState, useMemo } from 'react';

export const usePagination = (data, itemsPerPage = 10) => {
  const [currentPage, setCurrentPage] = useState(1);

  const paginatedData = useMemo(() => {
    // Ensure data is an array before calling slice
    if (!Array.isArray(data)) {
      return [];
    }
    const start = (currentPage - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    return data.slice(start, end);
  }, [data, currentPage, itemsPerPage]);

  const totalPages = Math.ceil((Array.isArray(data) ? data.length : 0) / itemsPerPage);

  return {
    currentPage,
    setCurrentPage,
    paginatedData,
    totalPages,
  };
};