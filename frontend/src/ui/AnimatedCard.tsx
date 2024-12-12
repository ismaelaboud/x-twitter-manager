import React from 'react';
import { motion } from 'framer-motion';
import { cn } from '../lib/utils';

interface AnimatedCardProps {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
}

export const AnimatedCard: React.FC<AnimatedCardProps> = ({ 
  children, 
  className, 
  hover = true 
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      whileHover={hover ? { scale: 1.02, transition: { duration: 0.2 } } : {}}
      className={cn(
        "bg-white shadow-md rounded-lg p-4 overflow-hidden",
        "transition-all duration-300 ease-in-out",
        hover && "hover:shadow-xl",
        className
      )}
    >
      {children}
    </motion.div>
  );
};
