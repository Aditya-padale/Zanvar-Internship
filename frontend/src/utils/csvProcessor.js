// src/utils/csvProcessor.js
import Papa from 'papaparse';

export const parseCSV = (file) => {
  return new Promise((resolve, reject) => {
    Papa.parse(file, {
      header: true,
      skipEmptyLines: true,
      complete: (results) => {
        resolve(results.data);
      },
      error: (error) => {
        reject(error);
      }
    });
  });
};

export const generateChartData = (csvData, columnName, chartType = 'bar') => {
  if (!csvData || !columnName || !csvData.length) {
    return null;
  }

  // Count occurrences of each value in the specified column
  const valueCounts = {};
  csvData.forEach(row => {
    const value = row[columnName];
    if (value) {
      valueCounts[value] = (valueCounts[value] || 0) + 1;
    }
  });

  const labels = Object.keys(valueCounts);
  const values = Object.values(valueCounts);

  // Generate colors
  const backgroundColors = labels.map((_, index) => 
    `hsla(${(index * 360 / labels.length)}, 70%, 60%, 0.8)`
  );
  const borderColors = labels.map((_, index) => 
    `hsla(${(index * 360 / labels.length)}, 70%, 50%, 1)`
  );

  return {
    labels,
    datasets: [{
      label: `Count of ${columnName}`,
      data: values,
      backgroundColor: chartType === 'pie' ? backgroundColors : backgroundColors[0],
      borderColor: chartType === 'pie' ? borderColors : borderColors[0],
      borderWidth: 1,
    }]
  };
};

export const getNumericColumns = (csvData) => {
  if (!csvData || !csvData.length) return [];
  
  const firstRow = csvData[0];
  return Object.keys(firstRow).filter(column => {
    // Check if the column contains mostly numeric values
    const numericValues = csvData.slice(0, 10).filter(row => 
      !isNaN(parseFloat(row[column])) && isFinite(row[column])
    );
    return numericValues.length > csvData.slice(0, 10).length * 0.7; // 70% numeric
  });
};

export const getCategoricalColumns = (csvData) => {
  if (!csvData || !csvData.length) return [];
  
  const firstRow = csvData[0];
  const numericColumns = getNumericColumns(csvData);
  
  return Object.keys(firstRow).filter(column => 
    !numericColumns.includes(column)
  );
};

export const generateLineChartData = (csvData, xColumn, yColumn) => {
  if (!csvData || !xColumn || !yColumn || !csvData.length) {
    return null;
  }

  const data = csvData
    .filter(row => row[xColumn] && row[yColumn])
    .map(row => ({
      x: row[xColumn],
      y: parseFloat(row[yColumn])
    }))
    .filter(point => !isNaN(point.y));

  return {
    labels: data.map(point => point.x),
    datasets: [{
      label: yColumn,
      data: data.map(point => point.y),
      borderColor: 'rgb(75, 192, 192)',
      backgroundColor: 'rgba(75, 192, 192, 0.2)',
      tension: 0.1
    }]
  };
};
