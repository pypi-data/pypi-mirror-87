..
    This file is part of Inspirehep.
    Copyright (C) 2016, 2017, 2018 CERN.

    Inspirehep is free software; you can redistribute it
    and/or modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation; either version 2 of the
    License, or (at your option) any later version.

    Inspirehep is distributed in the hope that it will be
    useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Inspirehep; if not, write to the
    Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
    MA 02111-1307, USA.

    In applying this license, CERN does not
    waive the privileges and immunities granted to it by virtue of its status
    as an Intergovernmental Organization or submit itself to any jurisdiction.


Changes
=======

Version 0.7.2
--------------

- Add new strategy `KEEP_HEAD_ENTITIES_CONFLICT_ON_NEW_UPDATE` which will create conflict when there is a new value in update.

Version 0.7.1
--------------

- Fix bug when DictMergeOps.keep_longest is used inside lists.

Version 0.7.0
--------------

- Add a new strategy for conflicts on head delete (contrib).

Version 0.6.1
--------------

- Smarter handling of conflicts in case of authors with the same name (contrib).

Version 0.6.0
--------------

- Correctly handle unicode in author names (contrib).

Version 0.5.2:
--------------

- Fix duplicate patches.

Version 0.5.1:
--------------

- Fix ``patch_to_conflict_set`` for list patches.

Version 0.5.0:
--------------

- Conflict method ``to_json`` it returns a list of patches conflicts of a single one.

Version 0.4.0:
--------------

- It's now possible to have field- and content- dependent merger operations.

Version 0.3.2:
--------------

- Initial public release.
