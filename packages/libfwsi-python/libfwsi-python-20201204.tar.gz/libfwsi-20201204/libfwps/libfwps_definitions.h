/*
 * The internal definitions
 *
 * Copyright (C) 2013-2019, Joachim Metz <joachim.metz@gmail.com>
 *
 * Refer to AUTHORS for acknowledgements.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

#if !defined( LIBFWPS_INTERNAL_DEFINITIONS_H )
#define LIBFWPS_INTERNAL_DEFINITIONS_H

#include <common.h>
#include <types.h>

/* Define HAVE_LOCAL_LIBFWPS for local use of libfwps
 */
#if !defined( HAVE_LOCAL_LIBFWPS )
#include <libfwps/definitions.h>

/* The definitions in <libfwps/definitions.h> are copied here
 * for local use of libfwps
 */
#else
#include <byte_stream.h>

#define LIBFWPS_VERSION				20191221

/* The version string
 */
#define LIBFWPS_VERSION_STRING			"20191221"

/* The byte order definitions
 */
#define LIBFWPS_ENDIAN_BIG			_BYTE_STREAM_ENDIAN_BIG
#define LIBFWPS_ENDIAN_LITTLE			_BYTE_STREAM_ENDIAN_LITTLE

/* The property value types
 */
enum LIBFWPS_VALUE_TYPES
{
	LIBFWPS_VALUE_TYPE_NAMED		= 1,
	LIBFWPS_VALUE_TYPE_NUMERIC		= 2
};

#endif

#endif

