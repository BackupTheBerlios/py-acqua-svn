/*#!/usr/bin/env python
# -*- coding: iso-8859-15 -*- 
#Copyright (C) 2005, 2006 Luca Sanna - Italy
#http://pyacqua.altervista.org
#email: pyacqua@gmail.com  
#
#   
#Py-Acqua is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#Py-Acqua is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Py-Acqua; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
*/
#include "stdio.h"     
#include "unistd.h"    
#include "sys/ioctl.h"
#include "fcntl.h"     
#include "time.h"     
#include "asm/etraxgpio.h"
#include <Python.h>
 
#define I2C_DATA_LINE   1<<24
#define I2C_CLOCK_LINE  1<<25
 
 
/* Area di implementazione */
 
int i2c_fd;
 
// Get the SDA line state
 
int i2c_getbit(void) {
  unsigned int value;
  value=ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_READBITS));
  if ((value&(I2C_DATA_LINE))==0) return 0;
  else return 1;
} 
 
// Set the SDA line as output
 
void i2c_dir_out(void) {
  int iomask;
  iomask = I2C_DATA_LINE;
  ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETGET_OUTPUT), &iomask);
}
 
// Set the SDA line as input
 
void i2c_dir_in(void) {
  int iomask;
  iomask = I2C_DATA_LINE;
  ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETGET_INPUT), &iomask);
}
 
// Set the SDA line state
 
void i2c_data(int state) {
  if (state==1) {
    i2c_dir_in(); 
  } else {  
    i2c_dir_out();  
    ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_CLRBITS), I2C_DATA_LINE);
  } 
}
 
// Set the SCL line state
 
void i2c_clk(int state) {
  if (state==1) ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETBITS), I2C_CLOCK_LINE);
  else ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_CLRBITS), I2C_CLOCK_LINE);
}
 
// Read a byte from I2C bus and send the ack sequence
// Put islast = 1 is this is the last byte to receive from the slave
 
unsigned char i2c_inbyte(int islast) {
  unsigned char value = 0;
  int bitvalue;
  int i;
 
  // Read data byte
 
  i2c_clk(0);
  i2c_dir_in();
 
  for (i=0;i<8;i++) {
    i2c_clk(1);
 
    bitvalue = i2c_getbit();
    value |= bitvalue;
    if (i<7) value <<= 1;
 
    i2c_clk(0);
  }
 
  if (islast==0) {
    // Send Ack if is not the last byte to read
 
    i2c_dir_out();
    i2c_data(0);
    i2c_clk(1);
    i2c_clk(0);
    i2c_dir_in();
  } else {
    // Doesn't send Ack if is the last byte to read
    i2c_dir_in();
    i2c_clk(1);
    i2c_clk(0);
  }
  return value;
}
 
 
// Open the GPIOB dev 
 
int i2c_open(void) {
  int iomask;
 
  i2c_fd = open("/dev/gpiog", O_RDWR);
  iomask = I2C_CLOCK_LINE;
  ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETGET_OUTPUT), &iomask);
  iomask = I2C_DATA_LINE;
  ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETGET_INPUT), &iomask);
  ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETBITS), I2C_DATA_LINE);
  i2c_dir_in();
  i2c_clk(1);
  return i2c_fd;
}
 
// Close the GPIOB dev 
 
void i2c_close(void) {
  i2c_dir_in();
  close(i2c_fd);
}
 
// Send a start sequence to I2C bus
 
void i2c_start(void){
  i2c_clk(0);
  i2c_data(1);
  i2c_clk(1);
  i2c_data(0);
}
 
// Send a stop sequence to I2C bus
 
void i2c_stop(void) {
  i2c_clk(0);
  i2c_data(0);
  i2c_clk(1);
  i2c_data(1);
}
 
// Send a byte to the I2C bus and return the ack sequence from slave
// rtc
//  0 = Nack, 1=Ack
 
int i2c_outbyte(unsigned char x) {
  int i;
  int ack;
 
  i2c_clk(0);
 
  for (i=0;i<8;i++) {
    if (x & 0x80) i2c_data(1);
    else  i2c_data(0);
    i2c_clk(1);
    i2c_clk(0);
    x <<= 1;
  }
 
  i2c_dir_in();
  i2c_clk(1);
  ack=i2c_getbit();
  i2c_clk(0);
 
  if (ack==0) return 1;
  else return 0;
}
 
/* Inizio codice wrapper */
 
static PyObject * wrap_i2c_getbit (PyObject *self, PyObject *args)
{
	return Py_BuildValue ("i", i2c_getbit ());
}
 

static PyMethodDef Foxi2cMethods[] = {
	
	{"i2c_getbit", wrap_i2c_getbit, METH_VARARGS, "Get the SDA line state"},
	{NULL, NULL, 0, NULL} // questa ha lo scopo di chiudere la tabella delle funzioni esportate
};
 

/* i2c_dir_out */
static PyObject * wrap_i2c_dir_out (PyObject *self, PyObject *args)
{
	return Py_BuildValue ("i", i2c_dir_out ());
}
static PyMethodDef Foxi2cMethods[] = {
	{"i2c_dir_out", wrap_i2c_dir_out, METH_VARARGS, "Set the SDA line as output"},
	{NULL, NULL, 0, NULL}
};

/* i2c_dir_in */
static PyObject * wrap_i2c_dir_in (PyObject *self, PyObject *args)
{
	return Py_BuildValue ("i", i2c_dir_in ());
}
static PyMethodDef Foxi2cMethods[] = {
	{"i2c_dir_in", wrap_i2c_dir_in, METH_VARARGS, "Set the SDA line as input"},
	{NULL, NULL, 0, NULL}
};

/* i2c_data */
static PyObject * wrap_i2c_data (PyObject *self, PyObject *args)
{
	return Py_BuildValue ("i", i2c_data ());
}
static PyMethodDef Foxi2cMethods[] = {
	{"i2c_data", wrap_i2c_data, METH_VARARGS, "Set the SDA line state"},
	{NULL, NULL, 0, NULL}
};

/* i2c_clk */
static PyObject * wrap_i2c_clk (PyObject *self, PyObject *args)
{
	return Py_BuildValue ("i", i2c_clk ());
}
static PyMethodDef Foxi2cMethods[] = {
	{"i2c_clk", wrap_i2c_clk, METH_VARARGS, "Set the SCL line state"},
	{NULL, NULL, 0, NULL}
};

/* i2c_inbyte */
static PyObject * wrap_i2c_inbyte (PyObject *self, PyObject *args)
{
	return Py_BuildValue ("i", i2c_inbyte ());
}
static PyMethodDef Foxi2cMethods[] = {
	{"i2c_inbyte", wrap_i2c_inbyte, METH_VARARGS, "Read a byte from I2C bus and send the ack sequence"},
	{NULL, NULL, 0, NULL}
};

/* i2c_open */
static PyObject * wrap_i2c_open (PyObject *self, PyObject *args)
{
	return Py_BuildValue ("i", i2c_open ());
}
static PyMethodDef Foxi2cMethods[] = {
	{"i2c_open", wrap_i2c_open, METH_VARARGS, "Open the GPIOB dev"},
	{NULL, NULL, 0, NULL}
};

/* i2c_close */
static PyObject * wrap_i2c_close (PyObject *self, PyObject *args)
{
	return Py_BuildValue ("i", i2c_close ());
}
static PyMethodDef Foxi2cMethods[] = {
	{"i2c_close", wrap_i2c_close, METH_VARARGS, "Close the GPIOB dev"},
	{NULL, NULL, 0, NULL}
};

/* i2c_start */
static PyObject * wrap_i2c_start (PyObject *self, PyObject *args)
{
	return Py_BuildValue ("i", i2c_start ());
}
static PyMethodDef Foxi2cMethods[] = {
	{"i2c_start", wrap_i2c_start, METH_VARARGS, "Send a start sequence to I2C bus"},
	{NULL, NULL, 0, NULL}
};

/* i2c_stop */
static PyObject * wrap_i2c_stop (PyObject *self, PyObject *args)
{
	return Py_BuildValue ("i", i2c_stop ());
}
static PyMethodDef Foxi2cMethods[] = {
	{"i2c_stop", wrap_i2c_stop, METH_VARARGS, "Send a stop sequence to I2C bus"},
	{NULL, NULL, 0, NULL}
};

/* i2c_outbyte */
static PyObject * wrap_i2c_outbyte (PyObject *self, PyObject *args)
{
	return Py_BuildValue ("i", i2c_outbyte ());
}
static PyMethodDef Foxi2cMethods[] = {
	{"i2c_outbyte", wrap_i2c_outbyte, METH_VARARGS, "Send a byte to the I2C bus and return the ack sequence from slave rtc"},
	{NULL, NULL, 0, NULL}
};
/* Ora passiamo a definire l'ultima funzione che serve ad inizializzare l'intero modulo */
PyMODINIT_FUNC
initfoxi2c (void)
{
	(void) Py_InitModule ("foxi2c", Foxi2cMethods);
}
