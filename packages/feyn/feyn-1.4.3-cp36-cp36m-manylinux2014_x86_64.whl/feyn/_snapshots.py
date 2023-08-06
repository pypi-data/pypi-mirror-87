from datetime import datetime
from typing import Union, List


class Snapshot:
    """
    A reference to a snapshot of a QLattice.

    The constructor is for internal use. You will normally access snapshots from the `SnapshotCollection` on a QLattice:
    >>> snapshot = qlattice.snapshots.capture("my snapshot")

    >>> for snapshot in qlattice.snapshots:
    >>>     print(snapshot.id)
    """
    def __init__(self, id: str, when: datetime, note: str):
        self._id = id
        self._when = when
        self._note = note

    @property
    def id(self):
        """A unique identifier for this snapshot"""
        return self._id

    @property
    def when(self):
        """A timestamp for when this snapshot was taken"""
        return self._when

    @property
    def note(self):
        """An optional note provided by the user when the snapshot was taken"""
        return self._note

    def __str__(self) -> str:
        return self.id

    def __repr__(self) -> str:
        return f"<Snapshot(id={self.id}, when={self.when}, note={self.note})>"


class SnapshotCollection():
    """
    The SnapshotCollection is used to capture, list and restore the state of a QLattice.

    Note: The actual snapshot is stored on the server side, so this collection manipulates references to these snapshots, including metadata about the snapshot.

    Use this collection to capture snapshots of the state of the QLattice:
    >>> snap = ql.snapshots.capture("Important lattice")

    And restore it again later:
    >>> ql.snapshots.restore(snap)

    It is also possible to treat the snapshot collection as a list:
    >>> for snap in ql.snapshots:
    >>>     print(snapshot.id, snapshot.when, snapshot.note)
    1587645521.535264 2020-04-21 11:28:31.535264+02:00 Some lattice
    1587645521.623532 2020-04-23 14:38:41.623532+02:00 Important lattice
    """

    def __init__(self, qlattice):
        self.qlattice = qlattice
        self._http_client = qlattice._http_client

    def capture(self, note: str) -> Snapshot:
        """
        Capture a snapshot of this QLattice.

        Arguments:
            note -- A note which is stored along with the snapshot.

        Returns:
            Snapshot -- A reference to the snapshot
        """
        resp = self._http_client.post("/snapshot", json={ "note": note })
        resp.raise_for_status()

        return self._snapshot_from_json(resp.json())

    def restore(self, snapshot: Union[str, Snapshot]):
        """
        Restore the QLattice to the state of a specific snapshot.

        Arguments:
            snapshot -- The snapshot the restore. Either a `Snapshot` instance returned from snapshots.capture() or a string id.
        """
        resp = self._http_client.post(f"/snapshot/{snapshot}/restore")

        if resp.status_code == 404:
            raise ValueError(f"No snapshot with id=[{snapshot}. Pick a Snapshot among the snapshots listed in `ql.snapshots`.")

        resp.raise_for_status()

        self.qlattice._load_qlattice()

    def __getitem__(self, index) -> Snapshot:
        return self._get_snapshot_list()[index]

    def __len__(self) -> int:
        resp = self._http_client.get("/snapshot")
        resp.raise_for_status()

        return len(resp.json())

    def __str__(self):
        return self._get_snapshot_list().__str__()

    def _get_snapshot_list(self) -> List[Snapshot]:
        resp = self._http_client.get("/snapshot")
        resp.raise_for_status()

        snapshots = [self._snapshot_from_json(s) for s in resp.json()]
        return sorted(snapshots, key=lambda s: s.when, reverse=False)

    def _snapshot_from_json(self, json) -> Snapshot:
        return Snapshot(
            json["id"],
            datetime.fromisoformat(json["when"]),
            json["note"]
        )
