import React from 'react';
import { ChevronLeft, ChevronRight } from '../../assets/icons';
import { Button } from './Button';

export const Pagination = ({
  currentPage,
  totalPages,
  onPageChange,
  siblingCount = 1,
}) => {
  const getPageNumbers = () => {
    const pages = [];
    const leftSibling = Math.max(1, currentPage - siblingCount);
    const rightSibling = Math.min(totalPages, currentPage + siblingCount);

    if (leftSibling > 2) {
      pages.push(1);
      pages.push('...');
    } else if (leftSibling === 2) {
      pages.push(1);
    }

    for (let i = leftSibling; i <= rightSibling; i++) {
      pages.push(i);
    }

    if (rightSibling < totalPages - 1) {
      pages.push('...');
      pages.push(totalPages);
    } else if (rightSibling === totalPages - 1) {
      pages.push(totalPages);
    }

    return pages;
  };

  return (
    <div className="flex items-center justify-center space-x-2 mt-4">
      <Button
        variant="ghost"
        size="sm"
        disabled={currentPage === 1}
        onClick={() => onPageChange(currentPage - 1)}
        icon={ChevronLeft}
      >
        Previous
      </Button>

      {getPageNumbers().map((page, index) => (
        <Button
          key={index}
          variant={page === currentPage ? 'primary' : 'ghost'}
          size="sm"
          onClick={() => typeof page === 'number' && onPageChange(page)}
          disabled={page === '...'}
          className={page === '...' ? 'cursor-default' : ''}
        >
          {page}
        </Button>
      ))}

      <Button
        variant="ghost"
        size="sm"
        disabled={currentPage === totalPages}
        onClick={() => onPageChange(currentPage + 1)}
        icon={ChevronRight}
        iconPosition="right"
      >
        Next
      </Button>
    </div>
  );
};